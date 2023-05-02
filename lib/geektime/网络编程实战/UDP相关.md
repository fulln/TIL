---
dg-publish: true
---

#java #极客时间 #UDP

## 06 | 嗨，别忘了UDP这个小兄弟

### 与TCP差异

1. UDP是数据报协议，tcp是面向"数据流"协议
2. TCP 是一个面向连接的协议，TCP 在 IP 报文的基础上，增加了诸如重传、确认、有序传输、拥塞控制等能力，通信的双方是在一个确定的上下文中工作的。
3. UDP 不保证报文的有效传递，不保证报文的有序，也就是说使用 UDP 的时候，我们需要做好丢包、重传、报文组装等工作。

### 使用场景

常见的 DNS 服务，SNMP 服务都是基于 UDP 协议的，这些场景对时延、丢包都不是特别敏感。另外多人通信的场景，如聊天室、多人游戏等，也都会使用到 UDP 协议。

### UDP编程

![](attachment/Pasted%20image%2020230308220201.png)


主要涉及函数

```C

#include <sys/socket.h>

ssize_t recvfrom(int sockfd, void *buff, size_t nbytes, int flags, 
　　　　　　　　　　struct sockaddr *from, socklen_t *addrlen); 

ssize_t sendto(int sockfd, const void *buff, size_t nbytes, int flags,
                const struct sockaddr *to, socklen_t addrlen); 
```


#### recvfrom

sockfd、buff 和 nbytes 是前三个参数。sockfd 是本地创建的套接字描述符，buff 指向本地的缓存，nbytes 表示最大接收数据字节。第四个参数 flags 是和 I/O 相关的参数，这里我们还用不到，设置为 0。后面两个参数 from 和 addrlen，实际上是返回对端发送方的地址和端口等信息，这和 TCP 非常不一样，TCP 是通过 accept 函数拿到的描述字信息来决定对端的信息。另外 UDP 报文每次接收都会获取对端的信息，也就是说报文和报文之间是没有上下文的。

#### sendto

sendto 函数中的前三个参数为 sockfd、buff 和 nbytes。sockfd 是本地创建的套接字描述符，buff 指向发送的缓存，nbytes 表示发送字节数。第四个参数 flags 依旧设置为 0。后面两个参数 to 和 addrlen，表示发送的对端地址和端口等信息。函数的返回值告诉我们实际发送的字节数。

	UDP 的每次接收和发送都是一个独立的上下文

### UDP使用注意

1. 如果没开启服务端，而在 UDP 程序里，则会一直阻塞在recvfrom上。
2. 在 UDP 服务器重启之后，继续进行报文的发送，这就是 UDP 报文“无上下文”的最好说明。



## 地址

此文章为3月day8 学习笔记，内容来源于极客时间《[06 | 嗨，别忘了UDP这个小兄弟 (geekbang.org)](https://time.geekbang.org/column/article/118122)》，推荐该课程
