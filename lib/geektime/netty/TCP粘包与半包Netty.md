---
dg-publish: true
title: TCP粘包与半包Netty
createTime: 2023-09-26 23:26
tags:
---
# TCP粘包与半包Netty

TCP是流式协议，消息无边界
### 粘包
1. 发送方每次写入数据 < 套接字缓冲区大小
2. 接收方读取套接字缓冲区数据不及时
### 半包

1. 发送方每次写入数据 > 套接字缓冲区大小
2. 发送数据大于协议的MTU，必须拆包

### 解决问题的手段： 找出消息边界

![[attachment/Pasted image 20230926233540.png]]


### netty对3种常见封帧支持
![[attachment/Pasted image 20230926233803.png]]

## 源码解读

### 核心工作流程

> io.netty.handler.codec.ByteToMessageDecoder#channelRead

```java
public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {  
    if (msg instanceof ByteBuf) {  
        selfFiredChannelRead = true;  
        CodecOutputList out = CodecOutputList.newInstance();  
        try {  
	        // 如果是第一笔数据，直接放累加器，不是就追加
            first = cumulation == null;  
            cumulation = cumulator.cumulate(ctx.alloc(),  
                    first ? Unpooled.EMPTY_BUFFER : cumulation, (ByteBuf) msg);  
            callDecode(ctx, cumulation, out);  
        } catch (DecoderException e) {  
            throw e;  
        } catch (Exception e) {  
            throw new DecoderException(e);  
        } finally {  
            try {  
                if (cumulation != null && !cumulation.isReadable()) {  
                    numReads = 0;  
                    try {  
                        cumulation.release();  
                    } catch (IllegalReferenceCountException e) {  
                        //noinspection ThrowFromFinallyBlock  
                        throw new IllegalReferenceCountException(  
                                getClass().getSimpleName() + "#decode() might have released its input buffer, " +  
                                        "or passed it down the pipeline without a retain() call, " +  
                                        "which is not allowed.", e);  
                    }  
                    cumulation = null;  
                } else if (++numReads >= discardAfterReads) {  
                    // We did enough reads already try to discard some bytes, so we not risk to see a OOME.  
                    // See https://github.com/netty/netty/issues/4275                    numReads = 0;  
                    discardSomeReadBytes();  
                }  
  
                int size = out.size();  
                firedChannelRead |= out.insertSinceRecycled();  
                fireChannelRead(ctx, out, size);  
            } finally {  
                out.recycle();  
            }  
        }  
    } else {  
        ctx.fireChannelRead(msg);  
    }  
}
```

# 地址

此文章为9月day26 学习笔记，内容来源于极客时间《https://time.geekbang.org/course/detail/100036701-151113》