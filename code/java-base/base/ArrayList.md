---
dg-publish: true
title: java基础之ArrayList
createTime: 2024-03-03 17:23
tags:
  - java
  - javabasic
  - datastruct
---
## 数据结构
- 默认容量大小10
- **modcount** (修改次数,保证fail-fast,线程不安全   
    - 通过对比modcount,如果不能对应,立即抛出并发修改异常
- 顶点接口
    - collection
- 循环
    - foreach循环
        - 不能在循环中对list进行增删操作.
            - fail-fast机制
    - fori循环
        - 可以在循环中对list进行增删操作
- Iterator
    - 迭代器,foreach循环的本质就是对迭代器进行循环
    - 通过Iterator的remove方法,可以进行删除操作
- randomAccess(可以快速访问随机的值
    - 每一个元素都可以通过内存地址（加偏移量） 进行快速的访问，这存取的时间复杂度为O(1)，称之为随机存储机制
- 顺序存储接口
## 主要方法
- add主要流程
    - 1.插入的位置不合理，直接抛出异常
    - 2.表长度小于插入后的长度，抛出异常或者动态扩容
    - 3.定位到要插入的i位置，将后面所有的向后移动一个位置
    - 4.将要插入的元素插入其中
    - 5.长度+1
- 删除
    - 使用的是system.arrayCopy进行数据的移动,将当前的桶index位置后所有位置往前挪动一位,然后将最后一位设置为null(等待gc
    - 检查参数的合法性
    - modcount+1
    - 获取到当前要删除的变量
- 1.8中`removeif`
    - [[ArrayList中removeif的源码实现分析]]

## 相关文档

[[lib/geektime/数据结构与算法/QUEUE|QUEUE]]
