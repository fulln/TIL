#datastruct #mysql #redis  

##  8种主要数据结构

![[Pasted image 20230129104007.png]]


-   Skiplist: a common in-memory index type. Used in Redis Skiplist：一种常见的内存索引类型。在 Redis 中使用
    
-   Hash index: a very common implementation of the “Map” data structure (or “Collection”) 哈希索引：“Map”数据结构（或“Collection”）的一种非常常见的实现
    
-   SSTable: immutable on-disk “Map” implementation SSTable：不可变的磁盘“映射”实现
    
-   LSM tree: Skiplist + SSTable. High write throughput LSM 树：Skiplist + SSTable。高写入吞吐量
    
-   B-tree: disk-based solution. Consistent read/write performance B-tree：基于磁盘的解决方案。一致的读/写性能
    
-   Inverted index: used for document indexing. Used in Lucene 倒排索引：用于文档索引。在 Lucene 中使用
    
-   Suffix tree: for string pattern search后缀树：用于字符串模式搜索
    
-   R-tree: multi-dimension search, such as finding the nearest neighbor R-tree：多维搜索，比如寻找最近邻