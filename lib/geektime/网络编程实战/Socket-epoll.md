---
dg-publish: true
---

#极客时间 #socket #epoll #io多路复用


# 23 | Linux利器：epoll的前世今生

如果说 I/O 多路复用帮我们打开了高性能网络编程的窗口，那么今天的主题——epoll，将为我们增添足够的动力。

![](https://static001.geekbang.org/resource/image/fd/60/fd2e25f72a5103ef78c05c7ad2dab060.png?wh=681*129)


### epoll的用法

#### epoll 本质上是IO多路复用的一种技术

不同于 poll 的是，epoll 不仅提供了默认的 ***level-triggered（条件触发）机制***，还提供了性能更为强劲的 ***edge-triggered（边缘触发）机制***。至于这两种机制的区别，我会在后面详细展开。

#### epoll  相关api

##### epoll_create

```c
int epoll_create(int size);
int epoll_create1(int flags);
        返回值: 若成功返回一个大于0的值，表示epoll实例；若返回-1表示出错
```

参数size 被自动忽略,但是仍然需要一个大于0 的值,当epoll实例不再需要,调用 close() 方法释放epoll 实例

现在内核可以动态分配需要的内核数据结构,这个参数size不在重要,但是仍然需要设置为大于1的值

##### epoll_ctl
```c
 int epoll_ctl(int epfd, int op, int fd, struct epoll_event *event);
        返回值: 若成功返回0；若返回-1表示出错
```

1. ` epfd` 是刚刚调用 epoll_create 创建的 epoll 实例描述字，可以简单理解成是 epoll 句柄。
2. `op `表示增加还是删除一个事件
	1. EPOLL_CTL_ADD： 向 epoll 实例注册文件描述符对应的事件；
	2. EPOLL_CTL_DEL：向 epoll 实例删除文件描述符对应的事件；
	3. EPOLL_CTL_MOD： 修改文件描述符对应的事件。
3.  `fd` 表示注册的事件的文件描述符
4. `*event` 注册的事件类型,并在这个结构中设置需要的数据,相关结构如下展示

```c
typedef union epoll_data {
     void        *ptr;
     int          fd;
     uint32_t     u32;
     uint64_t     u64;
 } epoll_data_t;

 struct epoll_event {
     uint32_t     events;      /* Epoll events */
     epoll_data_t data;        /* User data variable */
 };
```

**events:**

1. EPOLLIN：表示对应的文件描述字可以读;
2. EPOLLOUT：表示对应的文件描述字可以写；
3. EPOLLRDHUP：表示套接字的一端已经关闭，或者半关闭；
4. EPOLLHUP：表示对应的文件描述字被挂起；
5. EPOLLET：设置为 edge-triggered，默认为 level-triggered。

##### epoll_wait

```c

int epoll_wait(int epfd, struct epoll_event *events, int maxevents, int timeout);
  返回值: 成功返回的是一个大于0的数，表示事件的个数；返回0表示的是超时时间到；若出错返回-1.
  
```


1. `epfd`是 epoll 实例描述字，也就是 epoll 句柄。
2. `*events` 返回给用户空间需要处理的 I/O 事件，这是一个数组，数组的大小由 epoll_wait 的返回值决定,内容同`epoll-ctrl` 的入参
3. `maxevents`  epoll_wait 可以返回的最大事件值。
4. `timeout`  如果这个值设置为 -1，表示不超时；如果设置为 0 则立即返回，即使没有任何 I/O 事件发生。


#### edge-triggered VS level-triggered

对于 edge-triggered 和 level-triggered， 官方的说法是一个是边缘触发，一个是条件触发

> [!info]+ 区别
>条件触发的意思是只要满足事件的条件，比如有数据需要读，就一直不断地把这个事件传递给用户；而边缘触发的意思是只有第一次满足条件的时候才触发，之后就不会再传递同样的事件了。

**一般我们认为，边缘触发的效率比条件触发的效率要高，这一点也是 epoll 的杀手锏之一。**

#### epoll 的历史

Linus 在他最初的设想里，提到了这么一句话，也就是说他觉得类似 select 或 poll 的数组方式是可以的，而队列方式则是不可取的。

So sticky arrays of events are good, while queues are bad. Let’s take that as one of the fundamentals.

和最终的 epoll 实现相比，前者类似 epoll_ctl，后者类似 epoll_wait，不过原始的设计里没有考虑到创建 epoll 句柄，在最终的实现里增加了 epoll_create，支持了 epoll 句柄的创建。

### 总结

Linux 中 epoll 的出现，为高性能网络编程补齐了最后一块拼图。epoll 通过改进的接口设计，避免了用户态 - 内核态频繁的数据拷贝，大大提高了系统性能。



# 地址

此文章为4月day28 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/143245》

