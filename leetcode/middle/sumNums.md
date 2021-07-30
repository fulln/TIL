## 求1+2+…+n
求 1+2+...+n ，要求不能使用乘除法、for、while、if、else、switch、case等关键字及条件判断语句（A?B:C）。

 

示例 1：

输入: n = 3
输出: 6
示例 2：

输入: n = 9
输出: 45

```go
func sumNums(n int) int {
    ret :=0
    var add func(a,b int)bool
    add = func(a,b int)bool{
        sum ,arr := a^b, a&b
        ret = sum
        return arr > 0 && add(sum,arr << 1)  
    }
    var sum func(s int)bool    
    sum = func(s int)bool{
        add(ret,s)
        return s >0 && sum(s-1)
    }
    sum(n)
    return ret  
}



```
