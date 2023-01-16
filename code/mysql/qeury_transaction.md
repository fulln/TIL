#msyql #mysql运维

## mysql 事务锁相关查看

```sql

# 查看锁可获取情况
show status like 'Table%';

# 显示进程
show processlist;

# 查看正被使用的表
show open tables where  In_use >0;


-- 下面都需要更高级权限

# 查看事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX;

# 查看当前被锁定的事务
SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;

#查看事务执行
select r.trx_isolation_level, r.trx_id waiting_trx_id,r.trx_mysql_thread_id waiting_trx_thread,
r.trx_state waiting_trx_state,lr.lock_mode waiting_trx_lock_mode,lr.lock_type waiting_trx_lock_type,
lr.lock_table waiting_trx_lock_table,lr.lock_index waiting_trx_lock_index,r.trx_query waiting_trx_query,
b.trx_id blocking_trx_id,b.trx_mysql_thread_id blocking_trx_thread,b.trx_state blocking_trx_state,
lb.lock_mode blocking_trx_lock_mode,lb.lock_type blocking_trx_lock_type,lb.lock_table blocking_trx_lock_table,
lb.lock_index blocking_trx_lock_index,b.trx_query blocking_query
from information_schema.innodb_lock_waits w inner join information_schema.innodb_trx b on b.trx_id=w.blocking_trx_id
inner join information_schema.innodb_trx r on r.trx_id=w.requesting_trx_id
inner join information_schema.innodb_locks lb on lb.lock_trx_id=w.blocking_trx_id
inner join information_schema.innodb_locks lr on lr.lock_trx_id=w.requesting_trx_id

```
