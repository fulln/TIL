## Alter Table 操作执行过程

最近在公司发版的时候翻车了,在上线前加到现在没有执行完发版前的sql,一看原来是Alter table 操作,这就不奇怪了,mysql的ALTER TABLE 操作的性能对大表而言是一个大问题
,其中在执行ALTER TABLE的操作步骤的过程,大部分都是

   * 用新的结构创建一张空表
   * 从旧表查出所有数据插入到新表中
   * 然后删除旧表

这样操作很消耗时间,如果内存不足够的情况下数据量又很多,而且还有很多索引,这个操作将消耗数小时甚至数天才能完成

### ALTER TABLE 中的列操作差别

ALTER TABLE 允许使用 ALTER COLUMN ,MODIFY COLUMN 和 CHANGE COLUMN 语句来进行修改列,但是这3种操作都是不一样的,如给一列修改默认值(基于mysql5.7)

* MODIFY COLUMN
  
  modify的时候是拷贝了整张表数据到了新表里面,所有的MODIFY 操作都将导致表的重建
  
* ALTER COLUMN  

  列的默认值信息实际上是存储在`.frm`文件中的,alter 只针对其`.frm`文件进行修改,修改默认值的时候不会涉及到表数据改动,也就不会重建表

* CHANGE COLUMN
  
  change操作与modify操作比较像,除了modify操作不能重命名列名,所以这种操作也会导致重建表
  
### 总结

ALTER TABLE操作是很让人痛苦的,大部分情况下进行ALTER TABLE还会锁表,并重建整张表,所以目前一般做法

* 使用`Online DDL`对表数据
* 在建表时具有良好的前瞻性,并保留相关字段
* 新建同名表,然后进行数据同步,再rename
