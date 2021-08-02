## kafka消息可靠性保证(一)

kafka 消息保证是老生常谈的事情, 总结都做了n遍, 现在结合源码(kakfa版本v2.6.2)再来一遍,可靠性是由3个部分来进行保证的

1. 消费者保证
2. 生产者保证
3. broker保证

### 生产者保证

生产者对应的包为client项目下,其中比较重要的包为

* **org.apache.kafka.clients.producer 包 **。
* **org.apache.kafka.common.record 包**。这个包下面是各种 Kafka 消息实体类，比如用于在内存中传输的 MemoryRecords 类以及用于在磁盘上保存的 FileRecords 类。
* **org.apache.kafka.common.network 包**。实现 Client 和 Broker 之间网络传输的重要机制。

#### 生产者的act机制

> 机制详细解释可以看 org.apache.kafka.clients.producer.ProducerConfig#ACKS_DOC

先看看act机制在producter中是如何起作用的

* act参数初始化

  > org.apache.kafka.clients.producer.KafkaProducer	

  我们在创建连接后会初始化一个kafka的生产者

 	```java
 	  /**
 	  	我们通常是调用的对应Factroy ,实现生产者的初始化,以便管理, 这里的源码部分就是mock创建生产者的部分
 	  	
 	 * 通过提供一组键值对作为配置来实例化生产者。有效的配置字符串
 	 * 记录在<a href="http://kafka.apache.org/documentation.html#producerconfigs">此处</a>。
 	 * 值可以是字符串或适当类型的对象（例如，数字配置将接受 * 字符串“42”或整数 42）。
 	 * <p>
 	 * 注意：创建 {@code KafkaProducer} 后，您必须始终 {@link #close()} 以避免资源泄漏。
 	 * @param configs   The producer configs 配置项
 	 *
 	 */
 	public KafkaProducer(final Map<String, Object> configs) {
 	    this(configs, null, null, null, null, null, Time.SYSTEM);
 	}
 	
 	// visible for testing
 	@SuppressWarnings("unchecked")
 	KafkaProducer(Map<String, Object> configs, //kafka配置项
 	              Serializer<K> keySerializer, // 序列化的key值
 	              Serializer<V> valueSerializer, //序列化的value值
 	              ProducerMetadata metadata, // 生产者jvm限制参数
 	              KafkaClient kafkaClient, // kafka的连接信息
 	              ProducerInterceptors<K, V> interceptors,// 自定义的生产者拦截器
 	              Time time // kafka的抽象的 时间接口
 	             ) {
 	    ProducerConfig config = new ProducerConfig(ProducerConfig.addSerializerToConfig(configs, keySerializer,
 	            valueSerializer));
 	    try {
 	        //...
 						//省略其他参数的初始化
 	        this.sender = newSender(logContext, kafkaClient, this.metadata);
 	        this.ioThread = new KafkaThread(ioThreadName, this.sender, true);
 	        this.ioThread.start();
 						//···
 	        log.debug("Kafka producer started");
 	    } catch (Throwable t) {
 	        // 如果已经构造了内部对象，则调用 close 方法这是为了防止资源泄漏。见卡夫卡-2121
 	        close(Duration.ofMillis(0), true);
 	        // 现在传播异常
 	        throw new KafkaException("Failed to construct kafka producer", t);
 	    }
 	}

可以看看ackl默认值设置是在哪里设置的:

1. 初始化`org.apache.kafka.clients.producer.ProducerConfig`的时候会在静态代码块中,初始ACK的参数默认值为1

```java
 		static {
           CONFIG = new ConfigDef().define(BOOTSTRAP_SERVERS_CONFIG, Type.LIST, Collections.emptyList(), new ConfigDef.NonNullValidator(), Importance.HIGH, CommonClientConfigs.BOOTSTRAP_SERVERS_DOC)
                                 // ... 省略
                                   .define(ACKS_CONFIG,
                                           Type.STRING,
                                           "1",
                                           in("all", "-1", "0", "1"),
                                           Importance.HIGH,
                                           ACKS_DOC)
                                 // ... 省略
     }
```

2. 初始化时如果有带用户自定义参数,调用`postProcessParsedConfig(),` 其中会调用`org.apache.kafka.clients.producer.ProducerConfig#maybeOverrideAcksAndRetries`

```java
   private void maybeOverrideAcksAndRetries(final Map<String, Object> configs) {
           // 将ack 中的all 参数转成-1
           final String acksStr = parseAcks(this.getString(ACKS_CONFIG));
           // 设置ack参数
           configs.put(ACKS_CONFIG, acksStr);
           // For idempotence producers, values for `RETRIES_CONFIG` and `ACKS_CONFIG` might need to be overridden.
           // 如果是幂等要求
           if (idempotenceEnabled()) {
               // 要设置为重试次数大于 0 缓存队列重试，
               // 类似 gossip协议 中的直接邮递(gossip -> Direct Mail)
               // 这边重试队列不会有溢出丢弃的情况(消息数据本身不是在list中)
               // 还是能在这一点保证最终一致性
               boolean userConfiguredRetries = this.originals().containsKey(RETRIES_CONFIG);
               if (this.getInt(RETRIES_CONFIG) == 0) {
                   throw new ConfigException("Must set " + ProducerConfig.RETRIES_CONFIG + " to non-zero when using the idempotent producer.");
               }
               //如果在这个场景下用户的自定义为null，将设置为Integer.MAX_VALUE
               configs.put(RETRIES_CONFIG, userConfiguredRetries ? this.getInt(RETRIES_CONFIG) : Integer.MAX_VALUE);
               //这个场景下 设置ack值为-1
               boolean userConfiguredAcks = this.originals().containsKey(ACKS_CONFIG);
               final short acks = Short.valueOf(acksStr);
               if (userConfiguredAcks && acks != (short) -1) {
                   throw new ConfigException("Must set " + ACKS_CONFIG + " to all in order to use the idempotent " +
                           "producer. Otherwise we cannot guarantee idempotence.");
               }
               configs.put(ACKS_CONFIG, "-1");
           }
       }
```

* act参数的使用

  主要是在`org.apache.kafka.clients.producer.KafkaProducer#doSend`方法中初始化到sender中

  ```java
  		/**
  		  创建一个kafka生产者请求
       * Create a produce request from the given record batches
       */
      private void sendProduceRequest(long now, int destination, short acks, int timeout, List<ProducerBatch> batches) {
          if (batches.isEmpty())
              return;
  				// 消息分区和内存记录的map
          Map<TopicPartition, MemoryRecords> produceRecordsByPartition = new HashMap<>(batches.size());
          final Map<TopicPartition, ProducerBatch> recordsByPartition = new HashMap<>(batches.size());
  				// ...  省略
          ProduceRequest.Builder requestBuilder = ProduceRequest.Builder.forMagic(minUsedMagic, acks, timeout,
                  produceRecordsByPartition, transactionalId);
          RequestCompletionHandler callback = response -> handleProduceResponse(response, recordsByPartition, time.milliseconds());
        // 在这边发送对应请求,判断是不是需要有response, ack =0。就是不需要resp的
        // 另外在 ProduceRequest中有设置对应ack参数
          ClientRequest clientRequest = client.newClientRequest(nodeId, requestBuilder, now, acks != 0,
                  requestTimeoutMs, callback);
          client.send(clientRequest, now);
          log.trace("Sent produce request to {}: {}", nodeId, requestBuilder);
      }
  ```

  然后在2处:

  1. 在kafka的`org.apache.kafka.clients.NetworkClient` 中有1处进行了对应判断

  ```java
  //1.  判断如果是expectResponse 即对应上面方法中的ack != 0,不等待返回值,
  private void handleCompletedSends(List<ClientResponse> responses, long now) {
          // if no response is expected then when the send is completed, return it
    			// 如果本来就不期望返回值,那么直接返回null
          for (Send send : this.selector.completedSends()) {
              InFlightRequest request = this.inFlightRequests.lastSent(send.destination());
              if (!request.expectResponse) {
                  this.inFlightRequests.completeLastSent(send.destination());
                  responses.add(request.completed(null, now));
              }
          }
      }
  ```

  2. 在`kafka.server.KafkaApis` 中有1处使用对应的值
  ```scala
      /**
        * broker中处理producer
        */
       def handleProduceRequest(request: RequestChannel.Request): Unit = {
         //... 先省略其他的代码
         def processingStatsCallback(processingStats: FetchResponseStats): Unit = {
           processingStats.foreach { case (tp, info) =>
             updateRecordConversionStats(request, tp, info)
           }
         }
    
         if (authorizedRequestInfo.isEmpty)
           sendResponseCallback(Map.empty)
         else {
           val internalTopicsAllowed = request.header.clientId == AdminUtils.AdminClientId
           
           // call the replica manager to append messages to the replicas
           // 将消息加到副本上面
           replicaManager.appendRecords(
             timeout = produceRequest.timeout.toLong,
             // broker 在这里设置对应ack 参数到副本上
             requiredAcks = produceRequest.acks,
             internalTopicsAllowed = internalTopicsAllowed,
             origin = AppendOrigin.Client,
             entriesPerPartition = authorizedRequestInfo,
             responseCallback = sendResponseCallback,
             recordConversionStatsCallback = processingStatsCallback)
         }
       
  ```
  
  然后在`kafka.cluster.Partition`用作了校验
  
  ```scala
  def appendRecordsToLeader(records: MemoryRecords, origin: AppendOrigin, requiredAcks: Int): LogAppendInfo = {
      val (info, leaderHWIncremented) = inReadLock(leaderIsrUpdateLock) {
        leaderLogIfLocal match {
          case Some(leaderLog) =>
           // 最小同步分片数量
            val minIsr = leaderLog.config.minInSyncReplicas
           // 当前同步分片数量
            val inSyncSize = inSyncReplicaIds.size
  					//如果上面2个参数不等又设置了ack  = -1 直接报错出去
            // Avoid writing to leader if there are not enough insync replicas to make it safe
            if (inSyncSize < minIsr && requiredAcks == -1) {
              throw new NotEnoughReplicasException(s"The size of the current ISR $inSyncReplicaIds " +
                s"is insufficient to satisfy the min.isr requirement of $minIsr for partition $topicPartition")
            }
  
            val info = leaderLog.appendAsLeader(records, leaderEpoch = this.leaderEpoch, origin,
              interBrokerProtocolVersion)
  
            // we may need to increment high watermark since ISR could be down to 1
            (info, maybeIncrementLeaderHW(leaderLog))
  
          case None =>
            throw new NotLeaderOrFollowerException("Leader not local for partition %s on broker %d"
              .format(topicPartition, localBrokerId))
        }
      }
  ```
  

#### 生产者的CP保证

* **ack设置为-1**

  在初始化sender的时候将act参数加入,确保开通的是强一致性的-1

```java
/*处理向 Kafka 集群发送生产请求的后台线程。 该线程发出元数据请求以更新其集群视图，然后将生产请求发送到适当的节点
 */
Sender newSender(LogContext logContext, //消息上下文,封装一些消息之外的信息,如groupid
                 KafkaClient kafkaClient,//client
                 ProducerMetadata metadata// 生产者对应启动jvm参数
                ) {
       				// ...
        short acks = configureAcks(producerConfig, log);
        return new Sender(logContext,
                client,
                metadata,
                this.accumulator,
                maxInflightRequests == 1,
                producerConfig.getInt(ProducerConfig.MAX_REQUEST_SIZE_CONFIG),
                acks, // 将该参数放入 生产者成员变量中,
                producerConfig.getInt(ProducerConfig.RETRIES_CONFIG),
                metricsRegistry.senderMetrics,
                time,
                requestTimeoutMs,
                producerConfig.getLong(ProducerConfig.RETRY_BACKOFF_MS_CONFIG),
                this.transactionManager,
                apiVersions);
    }

/**
		生产者的消息强一致性(CP)保证:参数方面
 *  会去校验ack的设置
 		发送消息的时候幂等 -> ack 机制需要设置为-1,即消息需要所有的broker 确认收到后才能确定为已发送.
 */
private static short configureAcks(ProducerConfig config, Logger log) {
  		 // 是不是用户自定义的ack参数
        boolean userConfiguredAcks = config.originals().containsKey(ProducerConfig.ACKS_CONFIG);

  			short acks = Short.parseShort(config.getString(ProducerConfig.ACKS_CONFIG));

        if (config.idempotenceEnabled()) {
          
            if (!userConfiguredAcks)
                log.info("Overriding the default {} to all since idempotence is enabled.", ProducerConfig.ACKS_CONFIG);
            else if (acks != -1)
                throw new ConfigException("Must set " + ProducerConfig.ACKS_CONFIG + " to all in order to use the idempotent " +
                        "producer. Otherwise we cannot guarantee idempotence.");
        }
        return acks;
    }
```

* **最小同步副本数量**

   min.insync.replicas ,全部副本N中,同步副本数量要占${N/2 + 1}个,小于该数量,便无法服务于强一致性

* **不允许非同步leader** 

  unclean.leader.election.enable,如果boker当前不是最新的同步的节点, 不允许担任leader

```scala
// 上面2个配置都是在对应的KafkaConfig中
private val configDef = {

    new ConfigDef()
			// ...省略其他配置
      /** ********* Zookeeper Configuration ***********/
      /** ********* General Configuration ***********/
      /************ Rack Configuration ******************/
      /** ********* Log Configuration ***********/      
  		// 默认是1
      .define(MinInSyncReplicasProp, INT, Defaults.MinInSyncReplicas, atLeast(1), HIGH, MinInSyncReplicasDoc)
      /** ********* Replication configuration ***********/
  		// 默认是false
      .define(UncleanLeaderElectionEnableProp, BOOLEAN, Defaults.UncleanLeaderElectionEnable, HIGH, 	UncleanLeaderElectionEnableDoc)
			// ..省略其他配置
  }
```



#### 生产者AP保证



### 消费者保证

消费者对应的包为client项目下,其中重点包和生产者类似

* **org.apache.kafka.clients.consumer 包 **

#### 消费场景设置

### broker保证

core项目就是我们常说的对应broker的源码部分,其中比较重点的几个包为 : 

- **log 包**。log 包中定义了 Broker 底层消息和索引保存机制以及物理格式。
- **controller 包**。controller 包实现的是 Kafka Controller 的所有功能，特别是里面的 KafkaController.scala 文件，它封装了 Controller 的所有事件处理逻辑。
- **coordinator 包下的 group 包代码。**当前，coordinator 包有两个子 package：group 和 transaction。前者封装的是 Consumer Group 所用的 Coordinator；后者封装的是支持 Kafka 事务的 Transaction Coordinator
- **network 包代码以及 server 包下的部分代码**。 SocketServer 实现了 Broker 接收外部请求的完整网络流程

#### borker 消息备份与同步



#### 分区与多副本策略





先看request,当前版本的是用scala实现的对应

~~~~scala
class Request(val processor: Int,//序号，即当前这个process是由哪个线程处理
                                   //当 Request 被后面的 I/O 线程处理完成后，还要依靠 Processor 线程发送 Response 给请求发送方，
                                   //因此，Request 中必须记录它之前是被哪个 Processor 线程接收的。
                val context: RequestContext,
                                   //请求的内容
                val startTimeNanos: Long,
                                   //请求创建的时间
                memoryPool: MemoryPool,
                                   //最大内存池是多少，用来限制request 无限用内存池
                @volatile private var buffer: ByteBuffer, //buffer缓冲区
                metrics: RequestChannel.Metrics  // metrics 是 Request 相关的各种监控指标的一个管理类。它里面构建了一个 Map，封装了所有的请求 JMX 指标
             ) extends BaseRequest {
    // These need to be volatile because the readers are in the network thread and the writers are in the request 全由request写入
    // handler threads or the purgatory threads
    @volatile var requestDequeueTimeNanos = -1L
    @volatile var apiLocalCompleteTimeNanos = -1L
    @volatile var responseCompleteTimeNanos = -1L
    @volatile var responseDequeueTimeNanos = -1L
    @volatile var messageConversionsTimeNanos = 0L
    @volatile var apiThrottleTimeMs = 0L
    @volatile var temporaryMemoryBytes = 0L
    @volatile var recordNetworkThreadTimeCallback: Option[Long => Unit] = None
		//组header 和 body
    val session = Session(context.principal, context.clientAddress)
    private val bodyAndSize: RequestAndSize = context.parseRequest(buffer)

    def header: RequestHeader = context.header
    def sizeOfBodyInBytes: Int = bodyAndSize.size

    //most request types are parsed entirely into objects at this point. for those we can release the underlying buffer. 大多数请求玩直接释放缓冲区就完事
    //some (like produce, or any time the schema contains fields of types BYTES or NULLABLE_BYTES) retain a reference
    //to the buffer. for those requests we cannot release the buffer early, but only when request processing is done.
    if (!header.apiKey.requiresDelayedAllocation) {
      releaseBuffer()
    }

    def requestDesc(details: Boolean): String = s"$header -- ${loggableRequest.toString(details)}"

    def body[T <: AbstractRequest](implicit classTag: ClassTag[T], @nowarn("cat=unused") nn: NotNothing[T]): T = {
      bodyAndSize.request match {
        case r: T => r
        case r =>
          throw new ClassCastException(s"Expected request with type ${classTag.runtimeClass}, but found ${r.getClass}")
      }
    }

    def loggableRequest: AbstractRequest = {

      def loggableValue(resourceType: ConfigResource.Type, name: String, value: String): String = {
        val maybeSensitive = resourceType match {
          case ConfigResource.Type.BROKER => KafkaConfig.maybeSensitive(KafkaConfig.configType(name))
          case ConfigResource.Type.TOPIC => KafkaConfig.maybeSensitive(LogConfig.configType(name))
          case ConfigResource.Type.BROKER_LOGGER => false
          case _ => true
        }
        if (maybeSensitive) Password.HIDDEN else value
      }

      bodyAndSize.request match {
        case alterConfigs: AlterConfigsRequest =>
          val loggableConfigs = alterConfigs.configs().asScala.map { case (resource, config) =>
            val loggableEntries = new AlterConfigsRequest.Config(config.entries.asScala.map { entry =>
                new AlterConfigsRequest.ConfigEntry(entry.name, loggableValue(resource.`type`, entry.name, entry.value))
            }.asJavaCollection)
            (resource, loggableEntries)
          }.asJava
          new AlterConfigsRequest.Builder(loggableConfigs, alterConfigs.validateOnly).build(alterConfigs.version())

        case alterConfigs: IncrementalAlterConfigsRequest =>
          val resources = new AlterConfigsResourceCollection(alterConfigs.data.resources.size)
          alterConfigs.data.resources.forEach { resource =>
            val newResource = new AlterConfigsResource()
              .setResourceName(resource.resourceName)
              .setResourceType(resource.resourceType)
            resource.configs.forEach { config =>
              newResource.configs.add(new AlterableConfig()
                .setName(config.name)
                .setValue(loggableValue(ConfigResource.Type.forId(resource.resourceType), config.name, config.value))
                .setConfigOperation(config.configOperation))
            }
            resources.add(newResource)
          }
          val data = new IncrementalAlterConfigsRequestData()
            .setValidateOnly(alterConfigs.data().validateOnly())
            .setResources(resources)
          new IncrementalAlterConfigsRequest.Builder(data).build(alterConfigs.version)

        case _ =>
          bodyAndSize.request
      }
    }

    trace(s"Processor $processor received request: ${requestDesc(true)}")

    def requestThreadTimeNanos: Long = {
      if (apiLocalCompleteTimeNanos == -1L) apiLocalCompleteTimeNanos = Time.SYSTEM.nanoseconds
      math.max(apiLocalCompleteTimeNanos - requestDequeueTimeNanos, 0L)
    }

    def updateRequestMetrics(networkThreadTimeNanos: Long, response: Response): Unit = {
      val endTimeNanos = Time.SYSTEM.nanoseconds

      /**
       * Converts nanos to millis with micros precision as additional decimal places in the request log have low
       * signal to noise ratio. When it comes to metrics, there is little difference either way as we round the value
       * to the nearest long.
       */
      def nanosToMs(nanos: Long): Double = {
        val positiveNanos = math.max(nanos, 0)
        TimeUnit.NANOSECONDS.toMicros(positiveNanos).toDouble / TimeUnit.MILLISECONDS.toMicros(1)
      }

      val requestQueueTimeMs = nanosToMs(requestDequeueTimeNanos - startTimeNanos)
      val apiLocalTimeMs = nanosToMs(apiLocalCompleteTimeNanos - requestDequeueTimeNanos)
      val apiRemoteTimeMs = nanosToMs(responseCompleteTimeNanos - apiLocalCompleteTimeNanos)
      val responseQueueTimeMs = nanosToMs(responseDequeueTimeNanos - responseCompleteTimeNanos)
      val responseSendTimeMs = nanosToMs(endTimeNanos - responseDequeueTimeNanos)
      val messageConversionsTimeMs = nanosToMs(messageConversionsTimeNanos)
      val totalTimeMs = nanosToMs(endTimeNanos - startTimeNanos)
      val fetchMetricNames =
        if (header.apiKey == ApiKeys.FETCH) {
          val isFromFollower = body[FetchRequest].isFromFollower
          Seq(
            if (isFromFollower) RequestMetrics.followFetchMetricName
            else RequestMetrics.consumerFetchMetricName
          )
        }
        else Seq.empty
      val metricNames = fetchMetricNames :+ header.apiKey.name
      metricNames.foreach { metricName =>
        val m = metrics(metricName)
        m.requestRate(header.apiVersion).mark()
        m.requestQueueTimeHist.update(Math.round(requestQueueTimeMs))
        m.localTimeHist.update(Math.round(apiLocalTimeMs))
        m.remoteTimeHist.update(Math.round(apiRemoteTimeMs))
        m.throttleTimeHist.update(apiThrottleTimeMs)
        m.responseQueueTimeHist.update(Math.round(responseQueueTimeMs))
        m.responseSendTimeHist.update(Math.round(responseSendTimeMs))
        m.totalTimeHist.update(Math.round(totalTimeMs))
        m.requestBytesHist.update(sizeOfBodyInBytes)
        m.messageConversionsTimeHist.foreach(_.update(Math.round(messageConversionsTimeMs)))
        m.tempMemoryBytesHist.foreach(_.update(temporaryMemoryBytes))
      }

      // Records network handler thread usage. This is included towards the request quota for the
      // user/client. Throttling is only performed when request handler thread usage
      // is recorded, just before responses are queued for delivery.
      // The time recorded here is the time spent on the network thread for receiving this request
      // and sending the response. Note that for the first request on a connection, the time includes
      // the total time spent on authentication, which may be significant for SASL/SSL.
      recordNetworkThreadTimeCallback.foreach(record => record(networkThreadTimeNanos))

      if (isRequestLoggingEnabled) {
        val detailsEnabled = requestLogger.underlying.isTraceEnabled
        val responseString = response.responseString.getOrElse(
          throw new IllegalStateException("responseAsString should always be defined if request logging is enabled"))
        val builder = new StringBuilder(256)
        builder.append("Completed request:").append(requestDesc(detailsEnabled))
          .append(",response:").append(responseString)
          .append(" from connection ").append(context.connectionId)
          .append(";totalTime:").append(totalTimeMs)
          .append(",requestQueueTime:").append(requestQueueTimeMs)
          .append(",localTime:").append(apiLocalTimeMs)
          .append(",remoteTime:").append(apiRemoteTimeMs)
          .append(",throttleTime:").append(apiThrottleTimeMs)
          .append(",responseQueueTime:").append(responseQueueTimeMs)
          .append(",sendTime:").append(responseSendTimeMs)
          .append(",securityProtocol:").append(context.securityProtocol)
          .append(",principal:").append(session.principal)
          .append(",listener:").append(context.listenerName.value)
          .append(",clientInformation:").append(context.clientInformation)
        if (temporaryMemoryBytes > 0)
          builder.append(",temporaryMemoryBytes:").append(temporaryMemoryBytes)
        if (messageConversionsTimeMs > 0)
          builder.append(",messageConversionsTime:").append(messageConversionsTimeMs)
        requestLogger.debug(builder.toString)
      }
    }

    def releaseBuffer(): Unit = {
      if (buffer != null) {
        memoryPool.release(buffer)
        buffer = null
      }
    }

    override def toString = s"Request(processor=$processor, " +
      s"connectionId=${context.connectionId}, " +
      s"session=$session, " +
      s"listenerName=${context.listenerName}, " +
      s"securityProtocol=${context.securityProtocol}, " +
      s"buffer=$buffer)"

  }
~~~~



