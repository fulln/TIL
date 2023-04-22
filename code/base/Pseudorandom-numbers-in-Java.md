#java #javabasic #数据结构 

## Random and pseudorandom numbers are needed for everything from simulations to cryptography. Here’s how they work.

### What is randomness?

随机性是指不可预测或缺乏明确的模式或顺序的质量或状态。换句话说，随机性是事件或过程中预测性或规律性的缺失。例如，抛硬币是一个随机事件，因为无法确定它会落在正面还是反面。随机性是科学和数学许多领域中的基本概念，经常用于模拟复杂系统和生成各种目的的随机数。

用于安全目的的随机数必须极难被攻击者猜测。

#### 生成的速度
1. 随机数的速度是常见比较单位
2. 对一些只需要一个或几个随机数的普遍情况来说，速度没那么重要

#### 随机性
也就是生成的值如何可靠地分布在可能值的范围内

#### 可预测性

即外部人员知道某个调用将产生什么值的难度。低可预测性是密码学中使用的要求
[why cryptography requires the generation of random numbers](https://blog.cloudflare.com/why-randomness-matters/?source=:so:tw:or:awr:jav:::)

当涉及可预测性，周期是衡量数值在重复之前要求多少代。如果随机数生成器重复数值的速度太快，攻击者可能会以合理的精度猜出加密中使用的数值。


随机数生成器也可以是可跳跃的，也就是说，你应该能够在不破坏序列的情况下向前跳到一个时间点，相当于调用和丢弃一些操作。同样地，一个可跳跃的算法是可以在不破坏序列的情况下迈出一大步的算法。

#### 常见用途

1. 创建随机文件
```shell
someprogram > $ mktemp /tmp/scriptXXXXXXX
```

这样的文件为在公共目录中创建文件提供了一种合理的安全方式。甚至更好的系统也会将给每个运行的程序的进程ID号码随机化。这使得攻击者更难预测即将到来的命令的进程ID号码--这反过来又使得攻击系统更难。

### 真正的随机数与伪随机数的比较
大多数计算机没有真正的随机数，就像它们没有真正的实数一样；真正的随机数在计算上很昂贵（因此很耗时），而且通常不需要它们

Java早就提供了PRNG功能；Java 17对其功能进行了重大改变。

### java17 中的随机数

PRNG使用一种算法，它有一个起始值，即种子，和一个包络。常用的线性全能发生器（LCG）算法的包络部分是基于以下公式：

Xn+1 = (a * Xn + c) mod m

在这个公式中，X0是种子，每个值都是基于前一个值乘以一个常数a；这个结果加到另一个常数c上；然后将这个结果与第三个常数m相乘

#### 典型的IDE生成的hashCode方法
```JAVA
public class Datum {
    long id;
    String name;
    int yearJoined;

    @Override
    public int hashCode() {
        int result = (int) (id ^ (id >>> 32));
        result = 31 * result + (name != null ? name.hashCode() : 0);
        result = 31 * result + yearJoined;
        return result;
    }
    ...
}
```

改变状态会改变hashCode()的值，允许你更进一步地进行比较，如果你运行这个程序，你会发现它生成的数字看起来是随机的，但它们不是很好。


#### 问题点

1. 重复输出

如果你在选择前面显示的公式中的X0、a、m和c的值时作出非常糟糕的判断，例如，将X0、a和c都设为7，将m设为10，那么该公式将产生以下系列的输出：

7 6 9 0 7 6 9 0 7 6 9 0 ...

这个数列的重复周期为4，对大多数用途来说是完全无用的，**除非你真的知道你在做什么，否则不要实现你自己的LCG算法** 

2. 种子必须来自某处
在你测试随机数函数本身的罕见情况下，你可能希望种子是固定的（你可以将种子送入构造函数或使用setSeed()调用），这样，每次你运行测试时，算法将产生相同的数字集。

然而，在生产中使用随机数函数时，你希望种子是......等待它......随机的。这就需要使用另一个随机数函数，而这又需要从另一个随机数函数中获得自己的随机种子。你可以看到这将（或不会）结束的地方。

**只有一个不遵循固定算法的过程才能产生真正的随机数**


### 真正的随机数

One of the first computer-based true random number generators used Lavarand
> [!INFO] 一个设置在网络摄像头前的熔岩灯。熔岩灯包含两种不相溶的液体--蜡和一种透明液体，放在一个透明的直立容器中。来自白炽灯的热量使蜡上升，在那里冷却，然后下降，在一个无休止的循环中，每次都略有不同。

这个有点强：
a whole wall of lamps is used by internet backbone carrier Cloudflare to secure traffic on the current internet—really.

一些操作系统，如OpenBSD，从键盘、时间、环境中事物的安排等方面计算随机性（称为熵）。这样的操作系统在计算机关闭时将一些随机性保存在磁盘上，所以即使在操作系统第一次启动时，它已经有了一个很好的熵来源。目前，很少有其他操作系统能做到这一点


## 地址

https://blogs.oracle.com/javamagazine/post/java-pseudorandom-number-generator-background?source=:so:tw:or:awr:jav:::&SC=:so:tw:or:awr:jav:::&pcode=