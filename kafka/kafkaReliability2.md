## kafka消息可靠性保证(二)

kafka 消息保证是老生常谈的事情, 总结都做了n遍, 现在结合源码(kakfa版本v2.6.2)再来一遍,可靠性是由3个部分来进行保证的

1. 消费者保证
2. 生产者保证
3. broker保证

### 消费者保证

消费者对应的包为client项目下,其中重点包和生产者类似

* **org.apache.kafka.clients.consumer 包 **

#### 消费场景设置

* **autoCommit** vs **手动commit**

  1. enable.auto.commit = true

  > org.apache.kafka.clients.consumer.ConsumerConfig#ENABLE_AUTO_COMMIT_DOC

  ```java
    // 设置自动提交参数 的自定义, 如果没有设置就为false
    boolean maybeOverrideEnableAutoCommit() {
       		  // 获取group id 
            Optional<String> groupId = Optional.ofNullable(getString(CommonClientConfigs.GROUP_ID_CONFIG));
            // 获取系统中设置的自动提交参数
      			boolean enableAutoCommit = getBoolean(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG);
            
      			if (!groupId.isPresent()) { // overwrite in case of default group id where the config is not explicitly provided
              	// 默认false
                if (!originals().containsKey(ENABLE_AUTO_COMMIT_CONFIG)) {
                    enableAutoCommit = false;
                } else if (enableAutoCommit) {
                  // 没有设置groupId 不能自动提交
                    throw new InvalidConfigurationException(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG + " cannot be set to true when default group id (null) is used.");
                }
            }
            return enableAutoCommit;
        }
  ```

  2. auto.commit.interval.ms

  > org.apache.kafka.clients.consumer.ConsumerConfig#AUTO_COMMIT_INTERVAL_MS_DOC

  ```java
      	//默认值为5000 
     .define(AUTO_COMMIT_INTERVAL_MS_CONFIG,
                                             Type.INT,
                                             5000,
                                             atLeast(0),
                                             Importance.LOW,
                                             AUTO_COMMIT_INTERVAL_MS_DOC)
       //
  ```

  3. 偏移量提交

  > org.apache.kafka.clients.consumer.KafkaConsumer#poll(org.apache.kafka.common.utils.Timer, boolean)

     在consumer`poll` 拉取数据的时候,会有`coordinator.poll()`

  ```java
     private ConsumerRecords<K, V> poll(final Timer timer, final boolean includeMetadataInTimeout) {
             // 控制是当前线程消费的,非当前线程消费直接抛出异常
             acquireAndEnsureOpen();
             try {
                 // 消费者记录下消息消费的开始时间
                 this.kafkaConsumerMetrics.recordPollStart(timer.currentTimeMs());
     
                 if (this.subscriptions.hasNoSubscriptionOrUserAssignment()) {
                     throw new IllegalStateException("Consumer is not subscribed to any topics or assigned any partitions");
                 }
     
                 do {
                     // 消费者触发唤醒，看有没有唤醒，没有直接抛出异常
                     client.maybeTriggerWakeup();
     
                     if (includeMetadataInTimeout) {
                         // try to update assignment metadata BUT do not need to block on the timer for join group
                         updateAssignmentMetadataIfNeeded(timer, false);
                     } else {
                         // 同步消费者元数据，这里要通过coordinator 去同步出去
                        // 要是没有就 rebalance 加到这个group里面去
                         while (!updateAssignmentMetadataIfNeeded(time.timer(Long.MAX_VALUE), true)) {
                             log.warn("Still waiting for metadata");
                         }
                     }
     
                     final Map<TopicPartition, List<ConsumerRecord<K, V>>> records = pollForFetches(timer);
                     if (!records.isEmpty()) {
                         // before returning the fetched records, we can send off the next round of fetches
                         // and avoid block waiting for their responses to enable pipelining while the user
                         // is handling the fetched records.
                         //
                         // NOTE: since the consumed position has already been updated, we must not allow
                         // wakeups or any other errors to be triggered prior to returning the fetched records.
                         if (fetcher.sendFetches() > 0 || client.hasPendingRequests()) {
                             client.transmitSends();
                         }
     
                         return this.interceptors.onConsume(new ConsumerRecords<>(records));
                     }
                 } while (timer.notExpired());
     
                 return ConsumerRecords.empty();
             } finally {
                 release();
                 this.kafkaConsumerMetrics.recordPollEnd(timer.currentTimeMs());
             }
         }
     
     
     // coordinator.poll调用
     public boolean poll(Timer timer, boolean waitForJoinGroup) {
            ...
              // 先不管上面的逻辑
              // 在这里就回自动提交当前的消费的offset 
              //。具体就是掉send
             maybeAutoCommitOffsetsAsync(timer.currentTimeMs());
             return true;
         }
     
     // 异步提交偏移量
     private void doAutoCommitOffsetsAsync() {
             // 偏移量提交
             Map<TopicPartition, OffsetAndMetadata> allConsumedOffsets = subscriptions.allConsumed();
             log.debug("Sending asynchronous auto-commit of offsets {}", allConsumedOffsets);
     
             commitOffsetsAsync(allConsumedOffsets, (offsets, exception) -> {
                 if (exception != null) {
                     if (exception instanceof RetriableCommitFailedException) {
                         log.debug("Asynchronous auto-commit of offsets {} failed due to retriable error: {}", offsets,
                             exception);
                         nextAutoCommitTimer.updateAndReset(rebalanceConfig.retryBackoffMs);
                     } else {
                         log.warn("Asynchronous auto-commit of offsets {} failed: {}", offsets, exception.getMessage());
                     }
                 } else {
                     log.debug("Completed asynchronous auto-commit of offsets {}", offsets);
                 }
             });
         }
  ```

  4. rebalance 
     
     Kafka提供了一个角色：coordinator来执行对于consumer group的管理。坦率说kafka对于coordinator的设计与修改是一个很长的故事。最新版本的coordinator也与最初的设计有了很大的不同。这里我只想提及两次比较大的改变。
     
     首先是0.8版本的coordinator，那时候的coordinator是依赖zookeeper来实现对于consumer group的管理的。Coordinator监听zookeeper的`/consumers/<group>/ids`的子节点变化以及`/brokers/topics/<topic>`数据变化来判断是否需要进行rebalance。group下的每个consumer都自己决定要消费哪些分区，并把自己的决定抢先在zookeeper中的`/consumers/<group>/offsets/<topic>/<partition>`下注册。很明显，这种方案要依赖于zookeeper的帮助，而且每个consumer是单独做决定的，没有那种“大家属于一个组，要协商做事情”的精神。
     
     ```scala
     // 老版本和测试代码可以看到对应的定义,可见是在zookeeper上注册offsets
     def getConsumersOffsetsZkPath(consumerGroup: String, topic: String, partition: Int): String = {
           s"/consumers/$consumerGroup/offsets/$topic/$partition"
     }
     ```
     
     基于这些潜在的弊端，0.9版本的kafka改进了coordinator的设计，提出了group coordinator——每个consumer group都会被分配一个这样的coordinator用于组管理和位移管理。这个group coordinator比原来承担了更多的责任，比如组成员管理、位移提交保护机制等。当新版本consumer group的第一个consumer启动的时候，它会去和kafka server确定谁是它们组的coordinator。之后该group内的所有成员都会和该coordinator进行协调通信。显而易见，这种coordinator设计不再需要zookeeper了，性能上可以得到很大的提升。后面的所有部分我们都将讨论最新版本的coordinator设计。
     
     - 初始化
     
       ```java
       new ConsumerCoordinator(groupRebalanceConfig,
                               logContext,
                               this.client,
                               assignors,
                               this.metadata,
                               this.subscriptions,
                               metrics,
                               metricGrpPrefix,
                               this.time,
                               enableAutoCommit,
                               config.getInt(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG),
                               this.interceptors,
                               config.getBoolean(ConsumerConfig.THROW_ON_FETCH_STABLE_OFFSET_UNSUPPORTED));
       
       
       // 这里注重看下groupRebalanceConfig  这个属性
       public GroupRebalanceConfig(AbstractConfig config, ProtocolType protocolType) {
         		//。
               this.sessionTimeoutMs = config.getInt(CommonClientConfigs.SESSION_TIMEOUT_MS_CONFIG);
       
               // Consumer and Connect use different config names for defining rebalance timeout
         // 消费者和连接的使用的不同的rebalance timeout
               if (protocolType == ProtocolType.CONSUMER) {
                 // 使用的是max.poll.interval.ms 默认是5分钟
                   this.rebalanceTimeoutMs = config.getInt(CommonClientConfigs.MAX_POLL_INTERVAL_MS_CONFIG);
               } else {
                 //
                   this.rebalanceTimeoutMs = config.getInt(CommonClientConfigs.REBALANCE_TIMEOUT_MS_CONFIG);
               }
       
               ...
           }
       ```
     
     rebalance 触发条件一共有3种
     
      - 组成员发生变更(新consumer加入组、已有consumer主动离开组或已有consumer崩溃了)
      - 订阅主题数发生变更——这当然是可能的，如果你使用了正则表达式的方式进行订阅，那么新建匹配正则表达式的topic就会触发rebalance
      - 订阅主题的分区数发生变更     
     
     下面以加入组为例子看下rebalance的触发
     ```java
      @Override
         protected void onJoinPrepare(int generation, String memberId) {
             log.debug("Executing onJoinPrepare with generation {} and memberId {}", generation, memberId);
             // commit offsets prior to rebalance if auto-commit enabled
           // 该处的timeout 就是在上面设置好的 max.poll.interval.ms 
           // 如果还是在这个时间有效期内, 就一步自动提交一次offset
           // 校验 超时时间
             maybeAutoCommitOffsetsSync(time.timer(rebalanceConfig.rebalanceTimeoutMs));
     
             //出现错误或心跳超时时；在这种情况下，无论以前是什么
             //拥有的分区将丢失，我们应该触发回调并清理分配；
             //否则我们可以正常进行并根据协议撤销分区，
             //在这种情况下，我们应该仅在触发撤销回调后更改分配
             //因此用户仍然可以访问先前拥有的分区来提交偏移等。
     
             // the generation / member-id can possibly be reset by the heartbeat thread
             // upon getting errors or heartbeat timeouts; in this case whatever is previously
             // owned partitions would be lost, we should trigger the callback and cleanup the assignment;
             // otherwise we can proceed normally and revoke the partitions depending on the protocol,
             // and in that case we should only change the assignment AFTER the revoke callback is triggered
             // so that users can still access the previously owned partitions to commit offsets etc.
             Exception exception = null;
             final Set<TopicPartition> revokedPartitions;
             if (generation == Generation.NO_GENERATION.generationId &&
                 memberId.equals(Generation.NO_GENERATION.memberId)) {
                 revokedPartitions = new HashSet<>(subscriptions.assignedPartitions());
     
                 if (!revokedPartitions.isEmpty()) {
                     log.info("Giving away all assigned partitions as lost since generation has been reset," +
                         "indicating that consumer is no longer part of the group");
                     exception = invokePartitionsLost(revokedPartitions);
     
                     subscriptions.assignFromSubscribed(Collections.emptySet());
                 }
             } else {
               //在eager 的情况下直接重分配所有的分区
                 switch (protocol) {
                     case EAGER:
                         // revoke all partitions
                         revokedPartitions = new HashSet<>(subscriptions.assignedPartitions());
                         exception = invokePartitionsRevoked(revokedPartitions);
     
                         subscriptions.assignFromSubscribed(Collections.emptySet());
     
                         break;
     
                     case COOPERATIVE:
                     //在这种情况下,只处理不再订阅的分区
                         // only revoke those partitions that are not in the subscription any more.
                         Set<TopicPartition> ownedPartitions = new HashSet<>(subscriptions.assignedPartitions());
                         revokedPartitions = ownedPartitions.stream()
                             .filter(tp -> !subscriptions.subscription().contains(tp.topic()))
                             .collect(Collectors.toSet());
     
                         if (!revokedPartitions.isEmpty()) {
                             exception = invokePartitionsRevoked(revokedPartitions);
     
                             ownedPartitions.removeAll(revokedPartitions);
                             subscriptions.assignFromSubscribed(ownedPartitions);
                         }
     
                         break;
                 }
             }
     
             isLeader = false;
             subscriptions.resetGroupSubscription();
     
             if (exception != null) {
                 throw new KafkaException("User rebalance callback throws an error", exception);
             }
         }
     
     @Override
     protected void onJoinComplete(int generation,
                                       String memberId,
                                       String assignmentStrategy,
                                       ByteBuffer assignmentBuffer) {
             log.debug("Executing onJoinComplete with generation {} and memberId {}", generation, memberId);
     
             // Only the leader is responsible for monitoring for metadata changes (i.e. partition changes)
             // 只有leader 才可以修改元数据
             if (!isLeader)
                 assignmentSnapshot = null;
             // 查询Coordinator给消费者的分配策略 就是几个分区怎么分给几个消费者的
             //  如果没有，则提示策略异常
             ConsumerPartitionAssignor assignor = lookupAssignor(assignmentStrategy);
             if (assignor == null)
                 throw new IllegalStateException("Coordinator selected invalid assignment protocol: " + assignmentStrategy);
     
             // Give the assignor a chance to update internal state based on the received assignment
             // 获取消费者组内最新的元数据（包含几个消费者 offset到哪里了）
             groupMetadata = new ConsumerGroupMetadata(rebalanceConfig.groupId, generation, memberId, rebalanceConfig.groupInstanceId);
             // 这个消费者订阅的分区set
             Set<TopicPartition> ownedPartitions = new HashSet<>(subscriptions.assignedPartitions());
     
             // should at least encode the short version
             // 内容长度一看就不对
             if (assignmentBuffer.remaining() < 2)
                 throw new IllegalStateException("There are insufficient bytes available to read assignment from the sync-group response (" +
                     "actual byte size " + assignmentBuffer.remaining() + ") , this is not expected; " +
                     "it is possible that the leader's assign function is buggy and did not return any assignment for this member, " +
                     "or because static member is configured and the protocol is buggy hence did not get the assignment for this member");
             // 内容buffer转成对应实体
             Assignment assignment = ConsumerProtocol.deserializeAssignment(assignmentBuffer);
             //coordinator传过来的 订阅的分区set
             Set<TopicPartition> assignedPartitions = new HashSet<>(assignment.partitions());
             // 对比下 发现现在的订阅的分区 和 传过来的对不上， 就重新加入消费者组
             if (!subscriptions.checkAssignmentMatchedSubscription(assignedPartitions)) {
                 log.warn("We received an assignment {} that doesn't match our current subscription {}; it is likely " +
                     "that the subscription has changed since we joined the group. Will try re-join the group with current subscription",
                     assignment.partitions(), subscriptions.prettyString());
                 // 重新加入- 这里只是改值，后续有个
                 requestRejoin();
                 // 终止
                 return;
             }
     
     
             final AtomicReference<Exception> firstException = new AtomicReference<>(null);
             Set<TopicPartition> addedPartitions = new HashSet<>(assignedPartitions);
             addedPartitions.removeAll(ownedPartitions);
     
             // rebalance 协议
             //  EAGER  完全重新分配分区
             //  COOPERATIVE 消费者在下次rebalance之前保留其当前拥有的分区
             if (protocol == RebalanceProtocol.COOPERATIVE) {
                 Set<TopicPartition> revokedPartitions = new HashSet<>(ownedPartitions);
                 revokedPartitions.removeAll(assignedPartitions);
     
                 log.info("Updating assignment with\n" +
                         "\tAssigned partitions:                       {}\n" +
                         "\tCurrent owned partitions:                  {}\n" +
                         "\tAdded partitions (assigned - owned):       {}\n" +
                         "\tRevoked partitions (owned - assigned):     {}\n",
                     assignedPartitions,
                     ownedPartitions,
                     addedPartitions,
                     revokedPartitions
                 );
     
                 if (!revokedPartitions.isEmpty()) {
                     // Revoke partitions that were previously owned but no longer assigned;
                     // note that we should only change the assignment (or update the assignor's state)
                     // AFTER we've triggered  the revoke callback
                     firstException.compareAndSet(null, invokePartitionsRevoked(revokedPartitions));
     
                     // If revoked any partitions, need to re-join the group afterwards
                     log.debug("Need to revoke partitions {} and re-join the group", revokedPartitions);
                     // 重新加入消费组
                     requestRejoin();
                 }
             }
     
             // The leader may have assigned partitions which match our subscription pattern, but which
             // were not explicitly requested, so we update the joined subscription here.
             //在这边又同步下本地存的订阅信息
             maybeUpdateJoinedSubscription(assignedPartitions);
     
             // Catch any exception here to make sure we could complete the user callback.
             // 更新指定的信息
             firstException.compareAndSet(null, invokeOnAssignment(assignor, assignment));
     
             // Reschedule the auto commit starting from now
             // 自动提交 下次的自动提交时间
             if (autoCommitEnabled)
                 this.nextAutoCommitTimer.updateAndReset(autoCommitIntervalMs);
     
             subscriptions.assignFromSubscribed(assignedPartitions);
     
             // Add partitions that were not previously owned but are now assigned
             firstException.compareAndSet(null, invokePartitionsAssigned(addedPartitions));
     
             // 期间有报错没
             if (firstException.get() != null) {
                 if (firstException.get() instanceof KafkaException) {
                     throw (KafkaException) firstException.get();
                 } else {
                     throw new KafkaException("User rebalance callback throws an error", firstException.get());
                 }
             }
         }
     
     ```
     

  

  



