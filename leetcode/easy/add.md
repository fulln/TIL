##  不用加减乘除做加法


写一个函数，求两个整数之和，要求在函数体内不得使用 “+”、“-”、“*”、“/” 四则运算符号。

 

示例:

输入: a = 1, b = 1
输出: 2

```go
func add(a int, b int) int {
    var sum int
    var addFunc func(a,b int)bool
    addFunc  = func(a,b int)bool{
        sum = a^b
        total := a & b
        return total > 0 && addFunc(sum,total << 1)
    }
    addFunc(a,b)
    return sum
}

```
