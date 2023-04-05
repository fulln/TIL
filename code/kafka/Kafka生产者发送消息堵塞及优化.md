#kafka #queue #优化 #producer

## 地址链接

https://www.bilibili.com/video/BV1724y1j7HG/?spm_id_from=333.999.0.0&vd_source=1690412baac5d9ecc946844006611737

## 生产者发送消息可能阻塞么

1. producer发送的消息，先进入本地缓冲池中
	1. 缓冲池大小由 buffer.memory 控制，默认32M
	2. 缓存池分成多个大小相等batch，每个batch大小16kb，由batch.size 控制
2. 生产者将消息发送到不同的batch
3. 缓冲池内的batch 消耗完，则会阻塞发送线程
	1. **不会产生OOM** ，还是会慢慢发送。
	2. 因为缓冲池用完了会使用RecordAccumulator的内存，可能超过32M，就是会导致JVM的GC操作，比较消耗时间
4. 消息最终发送到Broker端的PageCache中
	1. send子线程按照batch异步发送到Broker，释放出batch空间
	2. 空闲batch 不用等待gc，快速堆积数据

## 如何优化

1. 测试生产环境中，生产者的QPS，向RecordAccumulator中写入数据，测试多久能写满
，设置合理的RecordAccumulator值
2. 设置合理的batchSize，
3. 一次request可以发送多条数据，`max.request.size`限制单个请求中的batch数量
4. Broker端单条消息大小调整大于`max.request.size`大小，Message.max.bytes 
5. 消费者端拉消息大小，fetch.max.size 

**max.request.size < message.max.bytes < fetch.max.size**