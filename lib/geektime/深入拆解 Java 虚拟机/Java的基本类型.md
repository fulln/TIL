#java #极客时间 #javabasic 

### Java 虚拟机的 boolean 类型

在java语言规范中,符号“true”和“false”是不能被虚拟机直接使用的

boolean 类型则被映射成 int 类型。具体来说，“true”被映射为整数 1，而“false”被映射为整数 0。这个编码规则约束了 Java 字节码的具体实现。

#### 汇编修改

1. AsmTools
2. ASM库
3. ...

### 基本类型

![[Pasted image 20230127180023.png]]


- char 类型的取值范围则是[0, 65535]。通常我们可以认定 char 类型的值为非负数
- 超过整数 0x7F800000 的被称为 NaN（Not-a-Number）。
- NaN 有一个有趣的特性：除了“!=”始终返回 true 之外，所有其他比较结果都会返回 false。

### 基本类型大小

#### 存储

- boolean、byte、char、short 这四种类型，在栈上占用的空间和 int 是一样的，和引用类型也是一样的。因此，在 32 位的 HotSpot 中，这些类型在栈上将占用 4 个字节；而在 64 位的 HotSpot 中，他们将占 8 个字节。
- 对于 byte、char 以及 short 这三种类型的字段或者数组单元，它们在堆上占用的空间分别为一字节、两字节，以及两字节
- int 存入上面的数组时,会进行掩码操作,将高位截取掉
- boolean数组是使用的byte数组实现,会进行掩码操作,只取最后一位值存入数组中.

#### 加载

- boolean、char 这两个无符号类型来说，加载伴随着零扩展,高位补0
- byte、short 这两个类型来说，加载伴随着符号扩展,如果是非负数则补0,否则补1

## 课程地址

[Java 的基本类型](https://time.geekbang.org/column/article/11503)