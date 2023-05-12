---
dg-publish: true
title: 手写高性能HTTP服务器（三）
createTime: 2023-05-12 21:35  
---

# 34 | 自己动手写高性能HTTP服务器（三）：TCP字节流处理和HTTP协议实现

### buffer 对象

如果是从套接字接收来的数据，事件处理回调函数在不断地往 buffer 对象增加数据，同时，应用程序需要不断把 buffer 对象中的数据处理掉，这样，buffer 对象才可以空出新的位置容纳更多的数据。

如果是发往套接字的数据，应用程序不断地往 buffer 对象增加数据，同时，事件处理回调函数不断调用套接字上的发送函数将数据发送出去，减少 buffer 对象中的写入数据。

![](https://static001.geekbang.org/resource/image/44/bb/44eaf37e860212a5c6c9e7f8dc2560bb.png?wh=946*316)


当 readIndex 和 writeIndex 越来越靠近缓冲的尾端时，前面部分的 front_space_size 区域变得会很大，而这个区域的数据已经是旧数据，在这个时候，就需要调整一下整个 buffer 对象的结构，把红色部分往左侧移动，与此同时，绿色部分也会往左侧移动，整个缓冲区的可写部分就会变多了。

### 套接字接收数据处理

套接字接收数据是在 tcp_connection.c 中的 handle_read 来完成的。在这个函数里，通过调用 buffer_socket_read 函数接收来自套接字的数据流，并将其缓冲到 buffer 对象中。

### 套接字发送数据处理

当应用程序需要往套接字发送数据时，即完成了 read-decode-compute-encode 过程后，通过往 buffer 对象里写入 encode 以后的数据，调用 tcp_connection_send_buffer，将 buffer 里的数据通过套接字缓冲区发送出去

### HTTP 协议实现

我们首先定义了一个 http_server 结构，这个 http_server 本质上就是一个 TCPServer，只不过暴露给应用程序的回调函数更为简单，只需要看到 http_request 和 http_response 结构。

```c

typedef int (*request_callback)(struct http_request *httpRequest, struct http_response *httpResponse);

struct http_server {
    struct TCPserver *tcpServer;
    request_callback requestCallback;
};
```

在 http_server 里面，重点是需要完成报文的解析，将解析的报文转化为 http_request 对象，这件事情是通过 http_onMessage 回调函数来完成的。在 http_onMessage 函数里，调用的是 parse_http_request 完成报文解析。

![](https://static001.geekbang.org/resource/image/6d/5a/6d91c7c2a0224f5d4bad32a0f488765a.png?wh=942*324)

处理完了所有的 request 数据，接下来进行编码和发送的工作。为此，创建了一个 http_response 对象，并调用了应用程序提供的编码函数 requestCallback，接下来，创建了一个 buffer 对象，函数 http_response_encode_buffer 用来将 http_response 中的数据，根据 HTTP 协议转换为对应的字节流。

# 地址

此文章为5月day12 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/155273》
