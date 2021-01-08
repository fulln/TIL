## Transaction resolution unknown 异常分析

生产遇到一堆异常,调来堆栈信息

```java
close connection error java.sql.SQLNonTransientConnectionException: Communications link failure during rollback(). Transaction resolution unknown.
		at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:110)
		at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:97)
		at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:89)
		at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:63)
		at com.mysql.cj.jdbc.ConnectionImpl.rollback(ConnectionImpl.java:1859)
		at com.mysql.cj.jdbc.ConnectionImpl.realClose(ConnectionImpl.java:1713)
		at com.mysql.cj.jdbc.ConnectionImpl.close(ConnectionImpl.java:717)
		at com.alibaba.druid.util.JdbcUtils.close(JdbcUtils.java:89)
		at com.alibaba.druid.pool.DruidDataSource.discardConnection(DruidDataSource.java:1487)
		at com.alibaba.druid.pool.DruidDataSource.getConnectionDirect(DruidDataSource.java:1415)
		at com.alibaba.druid.pool.DruidDataSource.getConnection(DruidDataSource.java:1375)
		at com.alibaba.druid.pool.DruidDataSource.getConnection(DruidDataSource.java:1365)
		at com.alibaba.druid.pool.DruidDataSource.getConnection(DruidDataSource.java:109)
		at org.springframework.jdbc.datasource.DataSourceUtils.fetchConnection(DataSourceUtils.java:151)
		at org.springframework.jdbc.datasource.DataSourceUtils.doGetConnection(DataSourceUtils.java:115)
		at org.springframework.jdbc.datasource.DataSourceUtils.getConnection(DataSourceUtils.java:78)
		at org.mybatis.spring.transaction.SpringManagedTransaction.openConnection(SpringManagedTransaction.java:82)
		at org.mybatis.spring.transaction.SpringManagedTransaction.getConnection(SpringManagedTransaction.java:68)
		at org.apache.ibatis.executor.BaseExecutor.getConnection(BaseExecutor.java:338)
		at org.apache.ibatis.executor.SimpleExecutor.prepareStatement(SimpleExecutor.java:84)
		at org.apache.ibatis.executor.SimpleExecutor.doQuery(SimpleExecutor.java:62)
		at org.apache.ibatis.executor.BaseExecutor.queryFromDatabase(BaseExecutor.java:326)
		at org.apache.ibatis.executor.BaseExecutor.query(BaseExecutor.java:156)
		at org.apache.ibatis.executor.CachingExecutor.query(CachingExecutor.java:109)
```

### 初步分析

首先拿到关键的异常日志

	Transaction resolution unknown.

google一番,发现大家都是说让手动commit下sqlsession,这种跟没有说一样,大家都是Spring自动管理的事务,哪里手动去commit,也犯不着,不过我顺着这个思路看了下driud 连接池的配置

```
min-idle: 5
initial-size: 10
max-active: 200
test-on-borrow: true
test-while-idle: true
validation-query: SELECT 1
min-evictable-idle-time-millis: 300000
keep-alive: true
defaultAutoCommit: false
``` 

看到一个奇怪的点,druid连接池配置将自动提交设置为了false,不让自动commit,但是我这边报错的基本都是查询相关的sql,根本用不上事务

### 进阶分析

没啥头绪,只能继续看堆栈有啥暴露的信息,因为上面参数的缘故,还是比较怀疑是druid的问题,先从这边入手,发现druid 调用`getConnectionDirect`获取连接后,就马上执行了`discardConnection`抛弃连接,那看下获取连接的操作:

```java
for (;;) {
            // handle notFullTimeoutRetry
            DruidPooledConnection poolableConnection;
            try {
                poolableConnection = getConnectionInternal(maxWaitMillis);
            } catch (GetConnectionTimeoutException ex) {
                if (notFullTimeoutRetryCnt <= this.notFullTimeoutRetryCount && !isFull()) {
                    notFullTimeoutRetryCnt++;
                    if (LOG.isWarnEnabled()) {
                        LOG.warn("get connection timeout retry : " + notFullTimeoutRetryCnt);
                    }
                    continue;
                }
                throw ex;
            }

            if (testOnBorrow) {
                boolean validate = testConnectionInternal(poolableConnection.holder, poolableConnection.conn);
                if (!validate) {
                    if (LOG.isDebugEnabled()) {
                        LOG.debug("skip not validate connection.");
                    }

                    Connection realConnection = poolableConnection.conn;
                    discardConnection(realConnection);
                    continue;
                }
            } else {
                Connection realConnection = poolableConnection.conn;
                if (poolableConnection.conn.isClosed()) {
                    discardConnection(null); // 传入null，避免重复关闭
                    continue;
                }

                if (testWhileIdle) {
                    final DruidConnectionHolder holder = poolableConnection.holder;
                    long currentTimeMillis             = System.currentTimeMillis();
                    long lastActiveTimeMillis          = holder.lastActiveTimeMillis;
                    long lastKeepTimeMillis            = holder.lastKeepTimeMillis;

                    if (lastKeepTimeMillis > lastActiveTimeMillis) {
                        lastActiveTimeMillis = lastKeepTimeMillis;
                    }

                    long idleMillis                    = currentTimeMillis - lastActiveTimeMillis;

                    long timeBetweenEvictionRunsMillis = this.timeBetweenEvictionRunsMillis;

                    if (timeBetweenEvictionRunsMillis <= 0) {
                        timeBetweenEvictionRunsMillis = DEFAULT_TIME_BETWEEN_EVICTION_RUNS_MILLIS;
                    }

                    if (idleMillis >= timeBetweenEvictionRunsMillis
                            || idleMillis < 0 // unexcepted branch
                            ) {
                        boolean validate = testConnectionInternal(poolableConnection.holder, poolableConnection.conn);
                        if (!validate) {
                            if (LOG.isDebugEnabled()) {
                                LOG.debug("skip not validate connection.");
                            }

                            discardConnection(realConnection);
                             continue;
                        }
                    }
                }
            }
		...
```

从这个方法里面可以看到我们设置连接参数几个参数,在判断完Maxwait,testOnBorrow,在判断当前连接跟数据库保持连接中失败. ,进入执行了discardConnet,最后调用了ConnectionImpl 中的realClose()

```java

 @Override
    public void close() throws SQLException {
        synchronized (getConnectionMutex()) {
            if (this.connectionLifecycleInterceptors != null) {
                for (ConnectionLifecycleInterceptor cli : this.connectionLifecycleInterceptors) {
                    cli.close();
                }
            }

            realClose(true, true, false, null);
        }
    }

...
 public void realClose(boolean calledExplicitly, boolean issueRollback, boolean skipLocalTeardown, Throwable reason) throws SQLException {
...

if (!skipLocalTeardown) {
                if (!getAutoCommit() && issueRollback) {
                    try {
                        rollback();
                    } catch (SQLException ex) {
                        sqlEx = ex;
                    }
                }
...
```

在这里我们可以发现, 如果我们没有设置为自动commit的时候,这个连接在关闭前会执行回滚,然而这个连接当前没有事务信息,所以会有

	Transaction resolution unknown

这个错误日志出来.这就是错误产生的直接原因. 那根本原因,然后解决办法呢

###  日志产生的原因分析

从之前的代码分析可以得到,由于testOnBorrow校验失败,才导致将当前连接放弃,这个校验失败就有很多种情况了, 如网络波动,超过了数据库的max_wait_time,数据库手动关了连接等等.这边生产库是TIDB的,我们直接是与TIDB中的TIDBserver集群连接.这里也就有HaProxy的连接问题,也可能会导致这个异常.

### 目前解决方法

快速的办法就是将autocommit设置为true,这样在关闭连接的时候不会前尝试rollback.从而避免这个异常的堆栈抛出.但是根本上的连接的异常,需要更多的时间去追踪下.
