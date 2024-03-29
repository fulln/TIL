---
dg-publish: true
---

## 课程内容

###  值对象和实体的本质区别

实体是靠独立于其他属性的标识来确定同一性的，而值对象以本身的值来确定同一性，没有独立于其他属性的标识；理论上，实体是可变的，而值对象是不可变的。

**实体之间的关系用关联来表达，而实体和值对象之间的关系用属性来表达**

#### 属性和关联的等价性

用属性表示对应关联关系

#### 属性要素的省略

UML 里的很多元素都是可以省略的，关键看你想强调什么。总的原则是，在表意清楚的前提下，尽量简洁

#### 如何在模型里表示值对象

DDD主要考虑的还是实体和实体之间的关系,一般情况下，实体之间的关系用关联来表达，而实体和值对象之间的关系用属性来表达。

- 值对象的基本表示方法
	- 枚举型值对象
	- 值对象的省略: 用| 表示有限态

- 值对象放在哪个包
	- 是依附实体的可以放聚合包,不是的可以放公共包

而值对象则是纯粹的概念产物，唯一的目的就是方便人的思考和沟通

>实体和值对象的本质区别在于，实体是人通过感官可以感觉到的客观存在的事物，或者以存在的事物为蓝本想象出来的事物；而值对象是为了描述事物，由人抽象出来的纯粹概念。讨论值对象的变化是没有意义的。

### 限定控制建模

假设有一个一对多的关联，如果表示“多”的一端的某一个属性被限定以后，可以变成一对一关联的话，那么就可以使用限定了

限定可以起到丰富模型语义和简化关联的作用。

	第一，表达了更丰富的语义，把原来用注解说明的约束变成了更严格的符号；
	第二，简化了关联关系的多重性，把原来的一对多，在形式上，变成了一对一。

#### 限定的各种使用

业务上特别强调要按照时间段来给项目成员分组。如果没有这样的需求，我们就不必使用限定了。

1. 唯一索引
2. map代码实现

在代码实现环节里实践 DDD，建议是写代码的同时一定要打开模型图，培养边看图边写代码的习惯。尤其是初学者更应该这么做，这样才能时刻提醒自己做到代码和模型的一致。

## 课程地址

[《手把手教你落地 DDD》学习笔记Day9](https://time.geekbang.org/column/article/623969)

[用“限定”建模：怎样简化一对多关联？](https://time.geekbang.org/column/article/624377)