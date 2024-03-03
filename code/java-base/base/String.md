---
createTime: 2024-03-03 19:39
tags:
  - java
  - javabasic
  - String
---
##  final类
- 1.保证hashcode不变
  - 2.避免被继承带来的隐患
  - 3.线程安全
  - 4.字符串池
	- 不同的字符串可以指向同一个字符串
##  和stringBuffer和StingBuilder区别
  - stringBuffer和stringBuilder是使用的append进行值得更改
  - stringBuffer 是线程安全的,在方法上使用了sync的关键字,stringBuilder是没有的
  - string是使用的+,是重新new了一个string然后进行赋值,它原本的值是无法更改的（效率上更高

## 解释String Pool

String Pool是Java中的一个特殊内存区域，用于存储所有由字面量创建的字符串。如果创建的字符串已经存在于池中，那么不会创建新的对象，而是直接引用池中的对象。