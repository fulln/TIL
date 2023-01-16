#mongodb #视频

## 视频地址

https://www.bilibili.com/video/BV1bJ411x7mq

## 概念 ☕

> MongoDB是一个开源, 高性能, 无模式的文档型数据库, 当初的设计就是用于简化开发和方便扩展, 是NoSQL数据库产品中的一种.是最 像关系型数据库（MySQL）的非关系型数据库. 它支持的数据结构非常松散, 是一种类似于 JSON 的 格式叫BSON, 所以它既可以存储比较复杂的数据类型, 又相当的灵活. MongoDB中的记录是一个文档, 它是一个由字段和值对（ﬁeld:value）组成的数据结构.MongoDB文档类似于JSON对象, 即一个文档认 为就是一个对象.字段的数据类型是字符型, 它的值除了使用基本的一些类型外, 还可以包括其他文档, 普通数组和文档数组.

## 特点

### 操作数据特点： [07:12](https://www.bilibili.com/video/BV1bJ411x7mq?p=2#t=432.381461)

1. 数据量大
2. 写入频繁
3. 价值较低的数据, 对**事务性**要求不高
4.  其他

### 使用特点：[04:50](https://www.bilibili.com/video/BV1bJ411x7mq?p=3#t=290.070723)

1. 高性能 ，主要是对嵌入式数据结构的支持，索引带来查询的高效，引擎满足各种场景
2. 高可用，副本集提供自动故障
3. 高扩展, 水平扩展，分片集群
4. 丰富查询支持，支持数据聚合，文本搜索

## 相关语法

### 部署与使用

1. shell脚本链接
2. compass 图形化界面
#### Linux 下的安装启动连接: [00:09](https://www.bilibili.com/video/BV1bJ411x7mq?p=6#t=9.092598)

1. mongoDb配置文件内容
>`vim /mongodb/single/mongo.conf `

```yaml
systemLog:
#MongoDB发送所有日志输出的目标指定为文件
#The path of the log file to which mongod or mongos should send all diagnostic logging
information
	destination: file
	#mongodi域ongos应向其发送所有诊断日志记录信息的日志文件的路径
	path: "/mongodb/single/log/mongod.log"
	#当mongos或nongod:实例重新启动时，mongos或mongod会将新条目附加到现有日志文件的末尾。
	logAppend: true
storage:
	#mongod实例存储其数据的目录。storage.dbPath设置仅适用于mongod。
	#The directory where the mongod instance stores its data.Default Value is "/data/db".
	dbPath: "/mongodb/single/data/db"
	journal:
		#启用或禁用特久性日志以确保数据文件保特有效和可恢复。
		enabled:true
processManagement:
	#启用在后台运行mongos或mongodi进程的守护进程模式。
	fork: true
net:
	#服务实例绑定的IP,默认是1oca7host
	bindIp: localhost,192.168.0.2
	#绑定的端口，默认是27017
	port: 27017
```

###  管理语法 : [01:45](https://www.bilibili.com/video/BV1bJ411x7mq?p=7#t=105.957478)

| 操作                                            | 语法                             | 备注                                                                                                                                                        | 对象                |
| ----------------------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 查看所有数据库                                  | `show dbs;` 或 `show databases;` | 有一些数据库名是保留的<br>  **admin** -> 权限库 <br>  **local** -> 数据永远不会被复制，存储本地单台服务器的任意集合<br>  **config** -> 用于保存分片相关信息 | 数据库 (databases)  |
| 查看当前数据库                                  | `db;`                            |                                                                                                                                                             | 数据库 (databases)  |
| 切换到某数据库 (**若数据库不存在则创建数据库**) | `   use <db_name>;`              |                                                                                                                                                             | 数据库 (databases)  |
| 删除当前数据库                                  | `   db.dropDatabase();`          |                                                                                                                                                             | 数据库 (databases)  |
| 查看所有集合                                    | `show collections;`              |                                                                                                                                                             | 集合（collections） |
| 创建集合                                        |       `db.createCollection("<collection_name>");`                           |                                                                                                                                                             |       集合（collections）               |
| 删除集合                                                |   `db.<collection_name>.drop()`                                |                                                                                                                                                             |         集合（collections）             |


### 针对文档的操作
1. 插入文档
> - 单条插入： `db.<collection_name>.insert()`  or `db.<collection_name>.save()` 
> - 多条插入：`db.<collection_name>.insertMany([])` 
> 🌟 插入时可以使用try-catch 捕获插入失败的数据

2.  查询单条文档：`db.<collection_name>.find()`

3. 更新文档 [00:49](https://www.bilibili.com/video/BV1bJ411x7mq?p=11#t=49.715298)
> 
 `db.<collection_name>.update(query,update,option，hint)`
>-  覆盖更新
>    直接传入Query，update entity，会直接覆盖已有数据
>- 局部更新
>   使用修改器`$set`: update
>- 批量更新
>  带参数`{multi:true}` 就更改多条数据了
>- 列值+1
> `{$inc:{}}`

4. 删除文档： `db.<collection_name>.remove(Query)`

5. 分页查询: 