#java #极客时间 

# 22 | 非阻塞I/O：提升性能的加速器

### 阻塞 VS 非阻塞

阻塞IO: 
内核所做的事情是将 CPU 时间切换给其他有需要的进程，网络应用程序在这种情况下就会得不到 CPU 时间做该做的事情。

非阻塞 I/O: 
当应用程序调用非阻塞 I/O 完成某个操作时，内核立即返回，不会把 CPU 时间切换给其他进程，应用程序在返回后，可以得到足够的 CPU 时间继续完成其他事情。

I/O 多路复用: 
每次通知对应线程去获取

非阻塞 I/O 可以被用到读操作、写操作、接收连接操作和发起连接操作上

### 非阻塞I/O

#### 读操作

在非阻塞情况下 read 调用会立即返回，一般返回 EWOULDBLOCK 或 EAGAIN 出错信息

#### 写操作
在阻塞 I/O 情况下，write 函数返回的字节数，和输入的参数总是一样的。

在非阻塞 I/O 的情况下，如果套接字的发送缓冲区已达到了极限，不能容纳更多的字节，那么操作系统内核会尽最大可能从应用程序拷贝数据到发送缓冲区中，并立即从 write 等函数调用中返回。可想而知，在拷贝动作发生的瞬间，有可能一个字符也没拷贝，有可能所有请求字符都被拷贝完成，那么这个时候就需要返回一个数值，告诉应用程序到底有多少数据被成功拷贝到了发送缓冲区中，应用程序需要再次调用 write 函数，以输出未完成拷贝的字节。

#### write函数的不一样：

非阻塞 I/O 需要这样：拷贝→返回→再拷贝→再返回。

而阻塞 I/O 需要这样：拷贝→直到所有数据拷贝至发送缓冲区完成→返回。

使用循环的方式来写入数据就好了。只不过在阻塞 I/O 的情况下，循环只执行一次就结束了。

#### read 和 write 在阻塞模式和非阻塞模式下的不同行为特性：

![](https://static001.geekbang.org/resource/image/6e/aa/6e7a467bc6f5985eebbd94ef7de14aaa.png?wh=1022*381)

read：
总是在接收缓冲区有数据时就立即返回，不是等到应用程序给定的数据充满才返回。当接收缓冲区为空时，阻塞模式会等待，非阻塞模式立即返回 -1，并有 EWOULDBLOCK 或 EAGAIN 错误。

write：
只有在发送缓冲区足以容纳应用程序的输出字节时才返回；而非阻塞模式下，则是能写入多少就写入多少，并返回实际写入的字节数。

write 调用会立即返回，并通过返回值告诉应用程序实际写入的字节数，如果再次对这样的套接字进行 write 操作，就会返回失败。失败是通过返回值 -1 来通知到应用程序的。

#### accept

当 accept 和 I/O 多路复用 select、poll 等一起配合使用时，如果在监听套接字上触发事件，说明有连接建立完成，此时调用 accept 肯定可以返回已连接套接字。这样看来，似乎把监听套接字设置为非阻塞，没有任何好处。

在监听套接字上有可读事件发生时，并没有马上调用 accept。由于客户端发生了 RST 分节，该连接被接收端内核从自己的已完成队列中删除了，此时再调用 accept，由于没有已完成连接（假设没有其他已完成连接），accept 一直阻塞，更为严重的是，该线程再也没有机会对其他 I/O 事件进行分发，相当于该服务器无法对其他 I/O 进行服务

**一定要将监听套接字设置为非阻塞的**

#### connect

在非阻塞 TCP 套接字上调用 connect 函数，会立即返回一个 EINPROGRESS 错误。TCP 三次握手会正常进行，应用程序可以继续做其他初始化的事情。当该连接建立成功或者失败时，通过 I/O 多路复用 select、poll 等可以进行连接的状态检测。

### 非阻塞 I/O + select 多路复用

```C

#define MAX_LINE 1024
#define FD_INIT_SIZE 128

char rot13_char(char c) {
    if ((c >= 'a' && c <= 'm') || (c >= 'A' && c <= 'M'))
        return c + 13;
    else if ((c >= 'n' && c <= 'z') || (c >= 'N' && c <= 'Z'))
        return c - 13;
    else
        return c;
}

//数据缓冲区
struct Buffer {
    int connect_fd;  //连接字
    char buffer[MAX_LINE];  //实际缓冲
    size_t writeIndex;      //缓冲写入位置
    size_t readIndex;       //缓冲读取位置
    int readable;           //是否可以读
};

struct Buffer *alloc_Buffer() {
    struct Buffer *buffer = malloc(sizeof(struct Buffer));
    if (!buffer)
        return NULL;
    buffer->connect_fd = 0;
    buffer->writeIndex = buffer->readIndex = buffer->readable = 0;
    return buffer;
}

void free_Buffer(struct Buffer *buffer) {
    free(buffer);
}

int onSocketRead(int fd, struct Buffer *buffer) {
    char buf[1024];
    int i;
    ssize_t result;
    while (1) {
        result = recv(fd, buf, sizeof(buf), 0);
        if (result <= 0)
            break;

        for (i = 0; i < result; ++i) {
            if (buffer->writeIndex < sizeof(buffer->buffer))
                buffer->buffer[buffer->writeIndex++] = rot13_char(buf[i]);
            if (buf[i] == '\n') {
                buffer->readable = 1;  //缓冲区可以读
            }
        }
    }

    if (result == 0) {
        return 1;
    } else if (result < 0) {
        if (errno == EAGAIN)
            return 0;
        return -1;
    }

    return 0;
}

int onSocketWrite(int fd, struct Buffer *buffer) {
    while (buffer->readIndex < buffer->writeIndex) {
        ssize_t result = send(fd, buffer->buffer + buffer->readIndex, buffer->writeIndex - buffer->readIndex, 0);
        if (result < 0) {
            if (errno == EAGAIN)
                return 0;
            return -1;
        }

        buffer->readIndex += result;
    }

    if (buffer->readIndex == buffer->writeIndex)
        buffer->readIndex = buffer->writeIndex = 0;

    buffer->readable = 0;

    return 0;
}

int main(int argc, char **argv) {
    int listen_fd;
    int i, maxfd;

    struct Buffer *buffer[FD_INIT_SIZE];
    for (i = 0; i < FD_INIT_SIZE; ++i) {
        buffer[i] = alloc_Buffer();
    }

    listen_fd = tcp_nonblocking_server_listen(SERV_PORT);

    fd_set readset, writeset, exset;
    FD_ZERO(&readset);
    FD_ZERO(&writeset);
    FD_ZERO(&exset);

    while (1) {
        maxfd = listen_fd;

        FD_ZERO(&readset);
        FD_ZERO(&writeset);
        FD_ZERO(&exset);

        // listener加入readset
        FD_SET(listen_fd, &readset);

        for (i = 0; i < FD_INIT_SIZE; ++i) {
            if (buffer[i]->connect_fd > 0) {
                if (buffer[i]->connect_fd > maxfd)
                    maxfd = buffer[i]->connect_fd;
                FD_SET(buffer[i]->connect_fd, &readset);
                if (buffer[i]->readable) {
                    FD_SET(buffer[i]->connect_fd, &writeset);
                }
            }
        }

        if (select(maxfd + 1, &readset, &writeset, &exset, NULL) < 0) {
            error(1, errno, "select error");
        }

        if (FD_ISSET(listen_fd, &readset)) {
            printf("listening socket readable\n");
            sleep(5);
            struct sockaddr_storage ss;
            socklen_t slen = sizeof(ss);
           int fd = accept(listen_fd, (struct sockaddr *) &ss, &slen);
            if (fd < 0) {
                error(1, errno, "accept failed");
            } else if (fd > FD_INIT_SIZE) {
                error(1, 0, "too many connections");
                close(fd);
            } else {
                make_nonblocking(fd);
                if (buffer[fd]->connect_fd == 0) {
                    buffer[fd]->connect_fd = fd;
                } else {
                    error(1, 0, "too many connections");
                }
            }
        }

        for (i = 0; i < maxfd + 1; ++i) {
            int r = 0;
            if (i == listen_fd)
                continue;

            if (FD_ISSET(i, &readset)) {
                r = onSocketRead(i, buffer[i]);
            }
            if (r == 0 && FD_ISSET(i, &writeset)) {
                r = onSocketWrite(i, buffer[i]);
            }
            if (r) {
                buffer[i]->connect_fd = 0;
                close(i);
            }
        }
    }
}
```



非阻塞 I/O 可以使用在 read、write、accept、connect 等多种不同的场景，在非阻塞 I/O 下，使用轮询的方式引起 CPU 占用率高，所以一般将非阻塞 I/O 和 I/O 多路复用技术 select、poll 等搭配使用，在非阻塞 I/O 事件发生时，再调用对应事件的处理函数。这种方式，极大地提高了程序的健壮性和稳定性，是 Linux 下高性能网络编程的首选。



# 地址

此文章为4月day26 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/141573》