---
dg-publish: true
title: # Java开发分布式存储系统
createTime: 2023-08-31 23:32  
---

# Java开发分布式存储系统

#### PageCache 调优和 Direct IO
PageCache，简单理解它就是内存。写内存性能肯定是最高的。但是 PageCache 并不是万能的，在某些情况下会存在命中率低，导致读写性能不高的情况。

>缓存的核心逻辑是：比如应用层要读 1KB 文件，那么内核的预读算法则会以它认为更合适的大小进行预读  I/O，比如 16-128KB。当应用程序下次读数据的时候，会先尝试读 PageCache，如果数据在 PageCache 中，就会直接返回；如果数据不在 PageCache 中，就会触发从硬盘读取数据，效率就会变低。

##### PageCache 无法起作用的场景

1. 使用 FIleChannel 读写时，底层可能走 Direct IO，不走页缓存。
2. 在内存有限或者不够用的时候，频繁换页，导致缓存命中率低。
3. 大量随机读的场景，导致页缓存的数据无法命中。

为了解决上面这类 PageCache 无法起作用的场景，有一种解决思路是：通过使用 Direct IO 来模拟实现 PageCahce 的效果。

**直接使用通过自定义 Cache + Direct IO 来实现更细致、自定义的管理内存、命中和换页等操作，从而针对我们的业务场景来优化缓存策略，从而实现比 PageCache 更好的效果。**

![](https://static001.geekbang.org/resource/image/d8/19/d86190bb6cfe6f3c0ba882335b71b219.jpg?wh=10666x6000)

NIO 中的 FileChannel 主要和 ByteBuffer 打交道，mmap 直接和缓存打交道，而 Direct IO 直接和硬盘打交道。即 Direct IO 是直接操作硬盘中的数据的，不经过应用缓存和页缓存。

**通过自定义 Cache 管理、缓存加载、换页等行为，让这些策略可以满足当前业务和场景的需求。**

Direct IO 可以通过 JNA/JNI 调用 Native 方法实来实现。GitHub 上有封装好了 Java JNA 库，实现了 Java 的 Direct IO，直接就可以使用。有兴趣的话，你可以去研究一下这个 GitHub 项目：https://github.com/smacke/jaydio。

### FileChannel 和 mmap

Java 原生的 IO 主要可以分为普通 IO、FileChannel（文件通道）、mmap（内存映射）三种。其中，java.io 包中的 FileWriter 和 FileReader 属于普通 IO；java.nio 包中的 FileChannel 属于 NIO 的一种；mmap 是调用 FileChannel.map() 实例出来的一种特殊读写文件的方式，被称为内存映射。基于字节传输的传统 IO 基本很少用了，当前主要使用 FileChannel 和 mmap。

```JAVA
FileChannel fileChannel = new RandomAccessFile(new File("test.data"), "rw").getChannel();

// 写数据
byte[] data = new byte[1024];
long position = 10L;
fileChannel.write(ByteBuffer.wrap(data)); //当前位置写入数据
fileChannel.write(ByteBuffer.wrap(data), position); //指定位置写入数据

// 读数据
ByteBuffer buffer = ByteBuffer.allocate(1024);
long position = 10L;
fileChannel.read(buffer); // 当前位置读取1024byte的数据
fileChannel.read(buffer,position)； // 指定位置读取 1024byte 的数据
```

FileChannel 写的时候经历了应用内存 -> PageCache -> 磁盘三个步骤。

![](https://static001.geekbang.org/resource/image/2e/b6/2e4c7986069cb2f423bd02ce2ef640b6.jpg?wh=10666x6000)

##### mmap基本使用

```java
MappedByteBuffer mappedByteBuffer = fileChannel.map(FileChannel.MapMode.READ_WRITE, 0, filechannel.size();

byte[] data = new byte[1024];
int position = 10;

// 从当前位置写入1kb的数据
mappedByteBuffer.put(data); 

// 从指定位置写入1kb的数据
MappedByteBuffer subBuffer = mappedByteBuffer.slice(); 
subBuffer.position(position);
subBuffer.put(data);
```

mmap 是一个把文件映射到内存的操作，因此可以像读写内存一样读写文件。它省去了用户空间到内核空间的数据复制过程，从而提高了读写性能。

>mmap 的写入也是先把数据写入到 PageCache，不是直接把数据写到硬盘中。它的底层借助了内存来加速，即 MappedByteBuffer 的 put 实际是对内存进行操作。具体刷盘依赖操作系统定时刷盘或者手动调用 mappedByteBuffer.force() 刷盘。

mmap 在内存充足、数据文件较小且相对固定的场景下，性能比 FileChannel 高。但它有这样几个缺点：

1. 使用时必须先指定好内存映射的大小，并且一次 Map 的大小限制在 1.5G 左右。
2. 是由操作系统来刷盘的，手动刷盘时间不好掌握。
3. 回收非常复杂，需要手动释放，并且代码和实现很复杂。

### 预分配文件、预初始化、池化

预分配文件是一个简单实用的优化技巧。比如前面讲过，消息队列的数据文件都是需要分段的，所以在创建分段文件的时候，可以预先写入空数据（比如 0）将文件预分配好。此时当我们真正写入业务数据的时候，速度就会快很多。

```JAVA
public void allocate(FileChannel fileChannel, 
long preFileSize) throw IOException{
    int bufferSize = 1024;
    ByteBuffer byteBuffer = ByteBuffer.allocateDirect(bufferSize);
    for (int i = 0; i < bufferSize; i++) {
        byteBuffer.put((byte)0);
    }
    byteBuffer.flip();
    long loop = preFileSize / bufferSize;
    for (long i = 0; i < loop; i++) {
        fileChannel.write(byteBuffer);
        byteBuffer.flip();
    }
    fileChannel.force(true);
    fileChannel.position(0);
}
```

对一些需要重复用到的对象或者实例化成本较高的对象进行预初始化，可以降低核心流程的资源开销。

还一点就是对象池化，对象池化是指只要是需要反复 new 出来的东西都可以池化，以避免内存分配后再回收，造成额外的开销。Netty 中的 Recycler、RingBuffer 中预先分配的对象都是按照这个池化的思路来实现的。



# 地址

此文章为8月day31 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/682691》