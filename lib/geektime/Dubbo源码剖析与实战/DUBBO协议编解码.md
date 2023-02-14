#java #dubbo #极客时间 

## 内容


Dubbo 的本质就是网络通信，要想把数据发到网络送往提供方，默认用 Netty 网络通信框架完成的
###  DUBBO协议编解码

#### 帧格式

根据不同协议规定的数据传输的格式

##### TCP/IP的帧格式

应用 -> 传输 -> 网络 -> 数据链路 -> 物理
![[Pasted image 20230212223143.png]]

##### 常规客户端 -> 服务端模拟

1. 固定长度
为了数据的接收齐全。client 和 server 进行了双方的约定，按照固定长度直接进行收发。server端收满固定的字节，不足长度的会舍弃

2. 分隔符
长度的设定比较重要， 短了，会增加访问的压力，长了，会造成资源的浪费，所以一般会约定特殊字符切割。

3. 定长+变长
约定数据格式由两部分组成，报文头、报文体。报文头是固定长度，里面有特殊的前缀标识、报文体的总长度；而报文体，长度是可变的，有多少数据就有多少长度。

##### DUBBO的数据帧格式

```JAVA

///////////////////////////////////////////////////                  
// org.apache.dubbo.remoting.exchange.codec.ExchangeCodec#encode
// 交换信息编解码操作，主要是将 Request、Response 对象按照 Dubbo 协议格式编码为字节流
///////////////////////////////////////////////////
@Override
public void encode(Channel channel, ChannelBuffer buffer, Object msg) throws IOException {
    // 如果是需要发送给提供方的对象，那么就调用 encodeRequest 进行编码
    if (msg instanceof Request) {
        encodeRequest(channel, buffer, (Request) msg);
    } 
    // 如果是响应给提供方的对象，那么就调用 encodeResponse 进行编码
    else if (msg instanceof Response) {
        encodeResponse(channel, buffer, (Response) msg);
    } 
    // 如果是其他类型对象的话，那么就调用父类的通用 encode 方法进行编码操作
    else {
        super.encode(channel, buffer, msg);
    }
}
```

主要分为3个部分，发送给request，发送给response，调用super的encode

###### request

```java

///////////////////////////////////////////////////                  
// 1、org.apache.dubbo.remoting.exchange.codec.ExchangeCodec#encodeRequest
// 2、将 Request 对象按照 Dubbo 协议格式编码为字节流
// 3、重点关注我在代码中描述的 ①②③④⑤⑥ 几个关键位置
///////////////////////////////////////////////////
// header length.
protected static final int HEADER_LENGTH = 16;
// magic header.
protected static final short MAGIC = (short) 0xdabb;
protected static final byte MAGIC_HIGH = Bytes.short2bytes(MAGIC)[0];
protected static final byte MAGIC_LOW = Bytes.short2bytes(MAGIC)[1];
// message flag.
protected static final byte FLAG_REQUEST = (byte) 0x80;
protected static final byte FLAG_TWOWAY = (byte) 0x40;
protected static final byte FLAG_EVENT = (byte) 0x20;
protected static final int SERIALIZATION_MASK = 0x1f;

// 将 Request 对象按照 Dubbo 协议格式编码为字节流
protected void encodeRequest(Channel channel, ChannelBuffer buffer, Request req) throws IOException {
    Serialization serialization = getSerialization(channel, req);
    // header.
    // ① 针对 header 字节数组赋值一个 0xdabb 魔术值
    byte[] header = new byte[HEADER_LENGTH];
    // set magic number.
    Bytes.short2bytes(MAGIC, header);
    
    // set request and serialization flag.
    // ② 设置序列化方式，序列化方式从 channel 的 url 取出 serialization 对应的参数值，
    // 默认是 hessian2 方式，
    // 而 org.apache.dubbo.common.serialize.hessian2.Hessian2Serialization#getContentTypeId 的值为 2
    // 
    // serialization 属性值，在源码中有如下这些值：
    // byte HESSIAN2_SERIALIZATION_ID = 2;
    // byte JAVA_SERIALIZATION_ID = 3;
    // byte COMPACTED_JAVA_SERIALIZATION_ID = 4;
    // byte FASTJSON_SERIALIZATION_ID = 6;
    // byte NATIVE_JAVA_SERIALIZATION_ID = 7;
    // byte KRYO_SERIALIZATION_ID = 8;
    // byte FST_SERIALIZATION_ID = 9;
    // byte NATIVE_HESSIAN_SERIALIZATION_ID = 10;
    // byte PROTOSTUFF_SERIALIZATION_ID = 12;
    // byte AVRO_SERIALIZATION_ID = 11;
    // byte GSON_SERIALIZATION_ID = 16;
    // byte PROTOBUF_JSON_SERIALIZATION_ID = 21;
    // byte PROTOBUF_SERIALIZATION_ID = 22;
    // byte KRYO_SERIALIZATION2_ID = 25;
    // byte MSGPACK_SERIALIZATION_ID = 27;    
    header[2] = (byte) (FLAG_REQUEST | serialization.getContentTypeId());
    
    // ③ 设置请求类型，根据 mTwoWay、mEvent 来决定是怎样的请求类型
    if (req.isTwoWay()) {
        header[2] |= FLAG_TWOWAY;
    }
    if (req.isEvent()) {
        header[2] |= FLAG_EVENT;
    }
    
    // ④ 设置请求唯一ID；
    // set request id.
    Bytes.long2bytes(req.getId(), header, 4);
    // encode request data.
    int savedWriteIndex = buffer.writerIndex();
    buffer.writerIndex(savedWriteIndex + HEADER_LENGTH);
    ChannelBufferOutputStream bos = new ChannelBufferOutputStream(buffer);
    
    // ⑤ 构建一个输出流，根据 mEvent 的值来将 mData 进行序列化转为字节数组
    if (req.isHeartbeat()) {
        // heartbeat request data is always null
        bos.write(CodecSupport.getNullBytesOf(serialization));
    } else {
        ObjectOutput out = serialization.serialize(channel.getUrl(), bos);
        if (req.isEvent()) {
            encodeEventData(channel, out, req.getData());
        } else {
            encodeRequestData(channel, out, req.getData(), req.getVersion());
        }
        out.flushBuffer();
        if (out instanceof Cleanable) {
            ((Cleanable) out).cleanup();
        }
    }
    bos.flush();
    bos.close();
    int len = bos.writtenBytes();
    checkPayload(channel, len);
    Bytes.int2bytes(len, header, 12);
    // write
    buffer.writerIndex(savedWriteIndex);
    buffer.writeBytes(header); // write header.
    
    // ⑥ 最终将序列化出来的字节数组的长度填充至报文体长度位置
    buffer.writerIndex(savedWriteIndex + HEADER_LENGTH + len);
}
```

可以看出 DUBBO的协议也是协议约定中“定长 + 变长”的实现版本。并且编码规则如下
![[Pasted image 20230212225328.png]]

1. 魔术高位：占用 8 bit，也就是 1 byte。该值固定为 0xda，是一种标识符。
2. 魔术地位：占用 8 bit，也就是 1 byte。该值固定为 0xbb，也是一种标识符。

魔术低位和魔术高位合并起来就是 0xdabb，代表着 dubbo 数据协议报文的开始。如果从通信 socket 收到的报文不是以 0xdabb 开始的，可以认为是非法报文。

3. 请求类和序列方式： 前面 4 bit 是请求类型，后面 4 bit 是序列化方式，合起来用 1 个 byte 来表示
4. 响应码：占用 8 bit，也是 1 byte。发出去的时候不用填这个值，响应回来就有值了，是 Dubbo 通信层面的错误码
5. request id：请求唯一 ID，占用 64 bit，也就是 8 byte。标识请求的唯一性，用来证明你收到的响应，就是你曾经发出去的请求返回来的数据。
6. ​body length：报文体长度，占用 32 bit，也就是 4 byte。体现真正的业务报文数据到底有多长。真实的业务有大有小，需要告诉读取多长字节
7. body content：报文体数据，占用的 bit 未知，占用的 byte 字节个数也未知。这里是我们真正业务数据的内容，至于真正的业务数据的长度有多长，完全由报文体长度决定。

#### 编解码的应用

实际开发中，如果需要自定义数据传输报文格式，也可以参照 Dubbo 的协议数据格式，稍加改造一番，然后自行通过代码编码和解码就可以了。

除了常见的dubbo协议编解码，还有

1. HTTP协议： 请求行 + 请求头 + 请求体构成的
2. RESP 协议，Redis 通信使用的协议，通过首字节的字符，来区分不同数据类型的序列化协议，甚至你都可以直接手写 Socket，把一段事先准备好的 RESP 报文调用 write 方法，就可以对 Redis 进行操作了。
3. WebSocket 协议，是 HTML5 的一种新型协议，实现了浏览器与服务器的全双工通信，本质还是基于 HTTP 协议的基础之上，借助 HTTP 协议来完成握手工作的


## 地址

此文章为2月day7 学习笔记，内容来源于极客时间《[22｜协议编解码：接口调用的数据是如何发到网络中的？ (geekbang.org)](https://time.geekbang.org/column/article/622433)》，推荐该课程



