#java #极客时间 #tcp 

##  04 | TCP三次握手：怎么使用套接字格式建立连接？

### TCP准备流程

####  初始化

```c
int socket(int domain, int type, int protocol)
```

domain: PF_INET、PF_INET6 以及 PF_LOCAL 等，表示什么样的套接字。

type:  
> SOCK_STREAM: 表示的是字节流，对应 TCP；
> SOCK_DGRAM： 表示的是数据报，对应 UDP；
> SOCK_RAW: 表示的是原始套接字。

protocol: protocol 原本是用来指定通信协议的，但现在基本废弃。因为协议已经通过前面两个参数指定完成。protocol 目前一般写成 0 即可。

#### bind

```c
bind(int fd, sockaddr *addr, socklen_t len)
```

通用地址格式sockaddr * addr: 虽然接收的是通用地址格式，实际上传入的参数可能是 IPv4、IPv6 或者本地套接字格式,bind 函数会根据 len 字段判断传入的参数 addr 该怎么解析

设置bind的时候，对应地址和端口有多种处理方式

1. 地址设置成本机的 IP 地址： 可以利用通配地址的能力
	- 对于 IPv4 的地址来说，使用 INADDR_ANY 来完成通配地址的设置；对于 IPv6 的地址来说，使用 IN6ADDR_ANY 来完成通配地址的设置。
	- 如果把端口设置成 0，就相当于把端口的选择权交给操作系统内核来处理，操作系统内核会根据一定的算法选择一个空闲的端口，完成套接字的绑定。这在服务器端不常使用。
2. 服务器端的程序一定要绑定到一个众所周知的端口上。服务器端的 IP 地址和端口数据   

#### listen

```c
int listen (int socketfd, int backlog)
```

通过 listen 函数，可以将原来的"主动"套接字转换为"被动"套接字，告诉操作系统内核：“我这个套接字是用来等待用户请求的。”

#### accept

操作系统内核需要把这个事件通知到应用程序，并让应用程序感知到这个连接

```c
int accept(int listensockfd, struct sockaddr *cliaddr, socklen_t *addrlen)
```

listen 套接字，这就是前面通过 bind，listen 一系列操作而得到的套接字.它是作为输入参数存在的；第二个是返回的已连接套接字描述字。

cliaddr: 第二个是返回的已连接套接字描述字,一旦一个客户和服务器连接成功，完成了 TCP 三次握手，操作系统内核就为这个客户生成一个已连接套接字，让应用服务器使用这个已连接套接字和客户进行通信处理

监听套接字一直都处于“监听”状态，等待新的客户请求到达并服务。

### 客户端发起连接的过程

#### connect

```c
int connect(int sockfd, const struct sockaddr *servaddr, socklen_t addrlen)
```

函数的第一个参数 sockfd 是连接套接字，通过前面讲述的 socket 函数创建。第二个、第三个参数 servaddr 和 addrlen 分别代表指向套接字地址结构的指针和该结构的大小。套接字地址结构必须含有服务器的 IP 地址和端口号。


客户在调用函数 connect 前不必非得调用 bind 函数，因为如果需要的话，内核会确定源 IP 地址，并按照一定的算法选择一个临时端口作为源端口。

##### 出错返回可能情况

1. 三次握手无法建立，客户端发出的 SYN 包没有任何响应，于是返回 TIMEOUT 错误。这种情况比较常见的原因是对应的服务端 IP 写错。
2. 客户端收到了 RST（复位）回答，这时候客户端会立即返回 CONNECTION REFUSED 错误。这种情况比较常见于客户端发送连接请求时的请求端口写错，因为 RST 是 TCP 在发生错误时发送的一种 TCP 分节。产生 RST 的三个条件是：目的地为某端口的 SYN 到达，然而该端口上没有正在监听的服务器（如前所述）；TCP 想取消一个已有连接；TCP 接收到一个根本不存在的连接上的分节。
3. 客户发出的 SYN 包在网络上引起了"destination unreachable"，即目的不可达的错误。这种情况比较常见的原因是客户端和服务器端路由不通。

### TCP三次握手解读

1. 服务器端通过 socket，bind 和 listen 完成了被动套接字的准备工作
2. 服务器端然后调用 accept，就会阻塞在这里，等待客户端的连接来临
3. 客户端通过调用 socket 和 connect 函数之后，也会阻塞

进入操作系统网络协议栈工作：

1. 客户端的协议栈向服务器端发送了 SYN 包，并告诉服务器端当前发送序列号 j，客户端进入 SYNC_SENT 状态；
2. 服务器端的协议栈收到这个包之后，和客户端进行 ACK 应答，应答的值为 j+1，表示对 SYN 包 j 的确认，同时服务器也发送一个 SYN 包，告诉客户端当前我的发送序列号为 k，服务器端进入 SYNC_RCVD 状态；
3. 客户端协议栈收到 ACK 之后，使得应用程序从 connect 调用返回，表示客户端到服务器端的单向连接建立成功，客户端的状态为 ESTABLISHED，同时客户端协议栈也会对服务器端的 SYN 包进行应答，应答数据为 k+1；
4. 应答包到达服务器端后，服务器端协议栈使得 accept 阻塞调用返回，这个时候服务器端到客户端的单向连接也建立成功，服务器端也进入 ESTABLISHED 状态。


## 地址

此文章为3月day6 学习笔记，内容来源于极客时间《[04 | TCP三次握手：怎么使用套接字格式建立连接？ (geekbang.org)](https://time.geekbang.org/column/article/116042)》，推荐该课程