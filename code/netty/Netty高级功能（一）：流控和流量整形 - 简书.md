---
title: Netty高级功能（一）：流控和流量整形 - 简书
url: https://www.jianshu.com/p/6c4a7cbbe2b5
date: 2024-02-27 11:24:20
tags:
  - netty
  - 流量控制
---
## Netty高级功能（一）：流控和流量整形

[![](https://upload.jianshu.io/users/upload_avatars/13194828/f3fc4a18-0044-414d-b33e-df4d3201225e.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/96/h/96/format/webp)](https://www.jianshu.com/u/ea8a81e1d960)

0.6372019.10.03 17:43:17字数 1,993阅读 14,316

这一章节，我们通过例子学习netty的一些高级特性。

## 1、netty客户端流控

在有些场景下，由于各种原因，会导致客户端消息发送积压，进而导致OOM。

-   1、当netty服务端并发压力过大，超过了服务端的处理能力时，channel中的消息服务端不能及时消费，这时channel堵塞，客户端消息就会堆积在发送队列中
-   2、网络瓶颈，当客户端发送速度超过网络链路处理能力，会导致客户端发送队列积压
-   3、当对端读取速度小于己方发送速度，导致自身TCP发送缓冲区满，频繁发生write 0字节时，待发送消息会在netty发送队列中排队

这三种情况下，如果客户端没有流控保护，这时候就很容易发生内存泄露。

##### 原因：

在我们调用channel的write和writeAndFlush时  
io.netty.channel.AbstractChannelHandlerContext#writeAndFlush(java.lang.Object, io.netty.channel.ChannelPromise)，如果发送方为业务线程，则将发送操作封装成WriteTask（继承Runnable），放到Netty的NioEventLoop中执行，当NioEventLoop无法完成如此多的消息的发送的时候，发送任务队列积压，进而导致内存泄漏。

##### 解决方案：

为了防止在高并发场景下，由于服务端处理慢导致的客户端消息积压，客户端需要做并发保护，防止自身发生消息积压。Netty提供了一个**高低水位机制，可以实现客户端精准的流控**。

io.netty.channel.ChannelConfig#setWriteBufferHighWaterMark 高水位  
io.netty.channel.ChannelConfig#setWriteBufferLowWaterMark 低水位

当发送队列待发送的字节数组达到高水位时，对应的channel就变为不可写状态，由于高水位并不影响业务线程调用write方法把消息加入到待发送队列，因此在消息发送时要先对channel的状态进行判断（ctx.channel().isWritable）。

这里涉及到的知识点是netty的消息发送机制。

##### netty的消息发送机制

业务调用write方法后，经过ChannelPipeline职责链处理，消息被投递到发送缓冲区待发送，调用flush之后会执行真正的发送操作，底层通过调用Java NIO的SocketChannel进行非阻塞write操作，将消息发送到网络上，

![](https://upload-images.jianshu.io/upload_images/13194828-cfe5197a9b93c156.png)

image.png

当用户线程（业务线程）发起write操作时，Netty会进行判断，如果发现不少NioEventLoop（I/O线程），则将发送消息封装成WriteTask，放入NioEventLoop的任务队列，由NioEventLoop线程执行，代码如下

io.netty.channel.AbstractChannelHandlerContext#write(java.lang.Object, io.netty.channel.ChannelPromise)

```
    @Override
    public ChannelFuture writeAndFlush(Object msg, ChannelPromise promise) {
        if (msg == null) {
            throw new NullPointerException("msg");
        }

        if (isNotValidPromise(promise, true)) {
            ReferenceCountUtil.release(msg);
            // cancelled
            return promise;
        }

        write(msg, true, promise);

        return promise;
    }

 private void write(Object msg, boolean flush, ChannelPromise promise) {
        AbstractChannelHandlerContext next = findContextOutbound();
        final Object m = pipeline.touch(msg, next);
        EventExecutor executor = next.executor();
        if (executor.inEventLoop()) {
            if (flush) {
                next.invokeWriteAndFlush(m, promise);
            } else {
                next.invokeWrite(m, promise);
            }
        } else {
            AbstractWriteTask task;
            if (flush) {
                task = WriteAndFlushTask.newInstance(next, m, promise);
            }  else {
                task = WriteTask.newInstance(next, m, promise);
            }
            safeExecute(executor, task, promise, m);
        }
    }
 private static void safeExecute(EventExecutor executor, Runnable runnable, ChannelPromise promise, Object msg) {
        try {
//这里的executor执行的是netty自己实现的SingleThreadEventExecutor#execute方法，
            executor.execute(runnable);
        } catch (Throwable cause) {
            try {
                promise.setFailure(cause);
            } finally {
                if (msg != null) {
                    ReferenceCountUtil.release(msg);
                }
            }
        }
    }

```

io.netty.util.concurrent.SingleThreadEventExecutor#execute

```
@Override
  public void execute(Runnable task) {
      if (task == null) {
          throw new NullPointerException("task");
      }

      boolean inEventLoop = inEventLoop();
      if (inEventLoop) {
          addTask(task);
      } else {
          startThread();
          addTask(task);
          if (isShutdown() && removeTask(task)) {
              reject();
          }
      }

      if (!addTaskWakesUp && wakesUpForTask(task)) {
          wakeup(inEventLoop);
      }
  }
```

Netty的NioEventLoop线程内部维护了一个Queue<Runnable> taskQuue，除了处理网络IO读写操作，同时还负责执行网络读写相关的Task，NioEventLoop遍历taskQueue，执行消息发送任务，代码调用入路径如下，具体的就不贴了，太长了  
io.netty.channel.nio.NioEventLoop#run  
\-----> io.netty.util.concurrent.SingleThreadEventExecutor#runAllTasks(long)  
\----->io.netty.util.concurrent.AbstractEventExecutor#safeExecute  
这里safeExecute执行的task，就是前面write写入时包装的AbstractWriteTask，AbstractWriteTask的run中  
io.netty.channel.AbstractChannelHandlerContext.AbstractWriteTask#run

经过一些系统处理操作，最终会调用io.netty.channel.ChannelOutboundBuffer#addMessage方法，将发送消息加入发送队列（链表）。

我们上面写的流程从NioSocketChannel到ChnnelOutbountBuffer，实际上在这个过程中，为了对发送速度和消息积压数进行控制，Netty还提供了高低水位机制，当消息队列中积压的待发送消息总字节数到达高水位时，修改Channel的状态为不可写，并发送通知事件；当消息发送完成后，对低水位进行判断，如果当前积压的待发送字节数低于低水位时，则修改channel状态为可写，并发送通知事件，具体代码见下  
io.netty.channel.ChannelOutboundBuffer#incrementPendingOutboundBytes(long)；  
io.netty.channel.ChannelOutboundBuffer#decrementPendingOutboundBytes(long)；

![](https://upload-images.jianshu.io/upload_images/13194828-39760969a8cfea07.png)

image.png

总结：在实际项目中，根据业务QPS规划，客户端处理性能、网络带宽、链路数、消息平均码流大小等综合因数，设置Netty高水位（setWriteBufferHighWaterMark）值，可以防止在发送队列处于高水位时继续发送消息，导致积压更严重，甚至发生内存泄漏。在系统中合理利用Netty的高低水位机制做消息发送的流控，既可以保护自身，同时又能减轻服务端的压力，可以提升系统的可靠性。

那么代码中，怎么使用呢？

![](https://upload-images.jianshu.io/upload_images/13194828-d7da33b270845a4f.png)

image.png

同时在业务发送消息时，添加socketChannel.isWritable()是否可以发送判断

```
    public static boolean sendMessage(String clientId,Object message){
        if(StringUtils.isEmpty(clientId)){
            log.error(" clientId 为空，找不到客户端！");
            return false;
        }
        SocketChannel socketChannel = FactoryMap.getChannelByDevNo(clientId);
        if(socketChannel !=null ){
            if(socketChannel.isWritable()){
                socketChannel.writeAndFlush(message);
                //更新数据库中消息状态
                return true;
            }else {
                log.error("channel不可写");
                return false;
            }
        }else {
            log.error(" 客户端未连接服务器！发送消息失败！{}",clientId);
        }
        return false;
    }
```

## 2、netty服务端 流量整形

前面讲的流控（高低水位控制），主要是根据发送消息队列积压的大小来控制客户端channel的写状态，然后用户手动根据channel.isWritable（）来控制消息是否发送，用户可以手动控制消息不能及时发送后的处理方案（比如，过期、超时）。通常用在客户端比较多。

流量整形呢，是一种主动调整流量输出速度的措施，一个典型的应用是基于下游网络节点的TPS指标控制本地流量的输出。大多数商用系统都由多个网元或者部件组成，例如参与短信互动，会涉及手机，基站，短信中心，短信网关，SP/CP等网元，不同网元或者部件的处理性能不同，为了防止突发的业务洪峰的 导致下游网元被冲垮，有时候需要消停提供流量整形功能。

![](https://upload-images.jianshu.io/upload_images/13194828-35d007e28df7b6d3.png)

image.png

Netty流量整形的主要作用：  
1、防止由于上下游网元性能不均衡导致下游网元被冲垮，业务流程中断；  
2、防止由于通信模块接收消息过快，后端业务线程处理不及时，导致出现“撑死”问题。  
例如，之前有博客的读者咨询过我一个问题，他们设备向服务端不间断的上报数据，有1G左右，而服务端处理不过来这么多数据，这种情况下，其实就可以使用流量整形来控制接收消息速度。

##### 原理和使用

原理：拦截channelRead和write方法，计算当前需要发送的消息大小，对读取和发送阈值进行判断，如果达到了阈值，则暂停读取和发送消息，待下一个周期继续处理，以实现在某个周期内对消息读写速度进行控制。

使用：将流量整形ChannelHandler添加到业务解码器之前，

![](https://upload-images.jianshu.io/upload_images/13194828-91a2bc7654c49ece.png)

image.png

##### 注意事项：

-   全局流量整形实例只需要创建一次  
    GlobalChannelTrafficShapingHandler 和 GlobalTrafficShapingHandler 是全局共享的，因此实例只需要创建一次，添加到不同的ChannelPipeline即可，不要创建多个实例，否则流量整形将失效。
    
-   流量整形参数调整不要过于频繁
    
-   **消息发送保护机制**  
    通过流量整形可以控制发送速度，但是它的控制原理是将待发送的消息封装成Task放入消息队列，等待执行时间到达后继续发送，所以如果业务发送线程不判断channle的可以状态，就可能会导致OOM问题。
    

最后编辑于

：2019.10.03 22:59:09

更多精彩内容，就在简书APP

![](https://upload.jianshu.io/images/js-qrc.png)

"小礼物走一走，来简书关注我"

还没有人赞赏，支持一下

[![  ](https://upload.jianshu.io/users/upload_avatars/13194828/f3fc4a18-0044-414d-b33e-df4d3201225e.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/100/h/100/format/webp)](https://www.jianshu.com/u/ea8a81e1d960)

总资产162共写了46.8W字获得1,351个赞共891个粉丝

-   序言：七十年代末，一起剥皮案震惊了整个滨河市，随后出现的几起案子，更是在滨河造成了极大的恐慌，老刑警刘岩，带你破解...
    
    [![](https://upload.jianshu.io/users/upload_avatars/15878160/783c64db-45e5-48d7-82e4-95736f50533e.jpg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)沈念sama](https://www.jianshu.com/u/dcd395522934)阅读 142,061评论 1赞 300
    
-   序言：滨河连续发生了三起死亡事件，死亡现场离奇诡异，居然都是意外死亡，警方通过查阅死者的电脑和手机，发现死者居然都...
    
-   文/潘晓璐 我一进店门，熙熙楼的掌柜王于贵愁眉苦脸地迎上来，“玉大人，你说我怎么就摊上这事。” “怎么了？”我有些...
    
-   文/不坏的土叔 我叫张陵，是天一观的道长。 经常有香客问我，道长，这世上最难降的妖魔是什么？ 我笑而不...
    
-   正文 为了忘掉前任，我火速办了婚礼，结果婚礼上，老公的妹妹穿的比我还像新娘。我一直安慰自己，他们只是感情好，可当我...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 48,601评论 1赞 255
    
-   文/花漫 我一把揭开白布。 她就那样静静地躺着，像睡着了一般。 火红的嫁衣衬着肌肤如雪。 梳的纹丝不乱的头发上，一...
    
-   那天，我揣着相机与录音，去河边找鬼。 笑死，一个胖子当着我的面吹牛，可吹牛的内容都是我干的。 我是一名探鬼主播，决...
    
-   文/苍兰香墨 我猛地睁开眼，长吁一口气：“原来是场噩梦啊……” “哼！你这毒妇竟也来了？” 一声冷哼从身侧响起，我...
    
-   想象着我的养父在大火中拼命挣扎，窒息，最后皮肤化为焦炭。我心中就已经是抑制不住地欢快，这就叫做以其人之道，还治其人...
    
-   序言：老挝万荣一对情侣失踪，失踪者是张志新（化名）和其女友刘颖，没想到半个月后，有当地人在树林里发现了一具尸体，经...
    
-   正文 独居荒郊野岭守林人离奇死亡，尸身上长有42处带血的脓包…… 初始之章·张勋 以下内容为张勋视角 年9月15日...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 29,234评论 2赞 214
    
-   正文 我和宋清朗相恋三年，在试婚纱的时候发现自己被绿了。 大学时的朋友给我发了我未婚夫和他白月光在一起吃饭的照片。...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 30,558评论 1赞 226
    
-   白月光回国，霸总把我这个替身辞退。还一脸阴沉的警告我。\[不要出现在思思面前， 不然我有一百种方法让你生不如死。\]我...
    
-   序言：一个原本活蹦乱跳的男人离奇死亡，死状恐怖，灵堂内的尸体忽然破棺而出，到底是诈尸还是另有隐情，我是刑警宁泽，带...
    
-   正文 年R本政府宣布，位于F岛的核电站，受9级特大地震影响，放射性物质发生泄漏。R本人自食恶果不足惜，却给世界环境...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 31,460评论 3赞 204
    
-   文/蒙蒙 一、第九天 我趴在偏房一处隐蔽的房顶上张望。 院中可真热闹，春花似锦、人声如沸。这庄子的主人今日做“春日...
    
-   文/苍兰香墨 我抬头看了看天上的太阳。三九已至，却和暖如春，着一层夹袄步出监牢的瞬间，已是汗流浃背。 一阵脚步声响...
    
-   我被黑心中介骗来泰国打工， 没想到刚下飞机就差点儿被人妖公主榨干…… 1. 我叫王不留，地道东北人。 一个月前我还...
    
-   正文 我出身青楼，却偏偏与公主长得像，于是被迫代替她去往敌国和亲。 传闻我的和亲对象是个残疾皇子，可洞房花烛夜当晚...
    
    [![](https://upload.jianshu.io/users/upload_avatars/4790772/388e473c-fe2f-40e0-9301-e357ae8f1b41.jpeg?imageMogr2/auto-orient/strip|imageView2/1/w/48/h/48/format/webp)茶点故事](https://www.jianshu.com/u/0f438ff0a55f)阅读 33,536评论 2赞 229
    

### 被以下专题收入，发现更多相似内容