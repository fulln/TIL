#DB #极客时间 

# 24 | RocksDB：不丢数据的高性能KV存储

RocksDB是 Facebook 开源的一个高性能持久化 KV 存储

### 同样是 KV 存储，RocksDB 有哪些不同？

1. RocksDB 采用了一个非常复杂的数据存储结构，并且这个存储结构采用了内存和磁盘混合存储方式，使用磁盘来保证数据的可靠存储，并且利用速度更快的内存来提升读写性能。或者说，RocksDB 的存储结构本身就自带了内存缓存。
2. RocksDB 它的数据结构，可以让绝大多数写入磁盘的操作都是顺序写
3. LSM-Tree

### LSM-Tree 如何兼顾读写性能？

![](https://static001.geekbang.org/resource/image/c0/6e/c0ba7aa330ea79a8a1dfe3a58547526e.jpg?wh=1187*841)


它包含了 WAL（Write Ahead Log）、跳表（SkipList）和一个分层的有序表（SSTable，Sorted String Table）

#### 写请求的操作

1. 写入到WALlog，是顺序写，性能很好
	1. wal日志唯一作用就是故障恢复
2. 数据写入到内存中的MemTable中，就是一个按照Key组织的跳表。跳表和平衡树有类似的查找性能，但是实现更简单。写操作速度非常快，写入到Memtable后就返回写入成功了
> [!info] LSM-Tree 在处理写入的过程中，直接就往 MemTable 里写，并不去查找这个 Key 是不是已经存在了。
	
 3. MemTable 太大了读写性能都会下降。所以，MemTable 有一个固定的上限大小，一般是 32M.写满之后，转换成了Immutable MemTable不允许写入，然后再创建一个空的 MemTable 继续写。
 4. 会后台程序不停的把Immutable MemTable 复制到磁盘文件中，然后释放内存空间。每个 Immutable MemTable 对应一个磁盘文件，MemTable 的数据结构跳表本身就是一个有序表，写入的文件也是一个按照 Key 排序的结构，这些文件就是 SSTable
 > [!INFO] 把 MemTable 写入 SSTable 这个写操作，因为它是把整块内存写入到整个文件中，这同样是一个顺序写操作。

5. SSTable 被分为很多层，越往上层，文件越少，越往底层，文件越多。每一层的容量都有一个固定的上限，一般来说，下一层的容量是上一层的 10 倍。当某一层写满了，就会触发后台线程往下一层合并，数据合并到下一层之后，本层的 SSTable 文件就可以删除掉了
6. 合并的过程也是排序的过程，除了 Level 0（第 0 层，也就是 MemTable 直接 dump 出来的磁盘文件所在的那一层。）以外，每一层内的文件都是有序的，文件内的 KV 也是有序的，这样就比较便于查找了。

#### 查询数据

先去内存中的 MemTable 和 Immutable MemTable 中找，然后再按照顺序依次在磁盘的每一层 SSTable 文件中去找，只要找到了就直接返回。这样的查找方式其实是很低效的，有可能需要多次查找内存和多个文件才能找到一个 Key，但实际的效果也没那么差，因为这样一个分层的结构，它会天然形成一个非常有利于查找的情况：越是被经常读写的热数据，它在这个分层结构中就越靠上，对这样的 Key 查找就越快。

在内存中缓存 SSTable 文件的 Key，用布隆过滤器避免无谓的查找等来加速查找过程。



# 地址

此文章为4月day5 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/225400》