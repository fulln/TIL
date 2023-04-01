#java #redis #mysql #极客时间 

# 17 | 大厂都是怎么做MySQL to Redis同步的?

### 缓存穿透：超大规模系统的不能承受之痛

不如把全量的数据都放在 Redis 集群里面，处理读请求的时候，干脆只读 Redis，不去读数据库。这样就完全没有“缓存穿透”的风险了，实际上很多大厂它就是这么干的。

#### 如何更新缓存中的数据

当系统更新数据库的数据之后，必须及时去更新缓存。

1. 分布式事务，对数据更新服务有侵入性
2. 如果redis本身出现故障，还是会导致下单失败。等于降低了下单服务性能和可用性

#### mq消息更新

**对于像订单服务这类核心的业务，一个可行的方法是，我们启动一个更新订单缓存的服务，接收订单变更的 MQ 消息，然后更新 Redis 中缓存的订单数据**

像 Kafka 或者 RocketMQ，它都有高可用和高可靠的保证机制，只要你正确配置好，是可以满足数据可靠性要求的。

#### Binlog 实时更新redis缓存

数据更新服务只负责处理业务逻辑，更新 MySQL，完全不用管如何去更新缓存。负责更新缓存的服务，把自己伪装成一个 MySQL 的从节点，从 MySQL 接收 Binlog，解析 Binlog 之后，可以得到实时的数据变更信息，然后根据这个变更信息去更新 Redis 缓存。

很多开源的项目就提供了订阅和解析 MySQL Binlog 的功能，我们以比较常用的开源项目Canal为例说明

1. 保证binlog格式
```
[mysqld]
log-bin=mysql-bin # 开启Binlog
binlog-format=ROW # 设置Binlog格式为ROW
server_id=1 # 配置一个ServerID
```

2. 给 Canal 开一个专门的 MySQL 用户并授权，确保这个用户有复制 Binlog 的权限：
```sql

CREATE USER canal IDENTIFIED BY 'canal';  
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';

FLUSH PRIVILEGES;
```

3. 检查binlog位置
![](https://static001.geekbang.org/resource/image/01/8f/01293d0ccc372418f3e01c785e204b8f.png?wh=1436*310)

4. 配置canal 配置文件，以连上Mysql
```properties
canal.instance.gtidon=false
# position info
canal.instance.master.address=127.0.0.1:3306
canal.instance.master.journal.name=binlog.000009
canal.instance.master.position=155
canal.instance.master.timestamp=
canal.instance.master.gtid=

# username/password
canal.instance.dbUsername=canal
canal.instance.dbPassword=canal
canal.instance.connectionCharset = UTF-8
canal.instance.defaultDatabaseName=test
# table regex
canal.instance.filter.regex=.*\\..
```

5. 启动canal服务
6.  启动客户端连接canal,并编写自己的业务代码


# 地址

此文章为4月day1 学习笔记，内容来源于极客时间《https://time.geekbang.org/column/article/217593》，