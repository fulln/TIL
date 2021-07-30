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
    var sum func(s int)bool
    m := 0
    sum = func(s int)bool{
        add(m,s)
        return s >0 && sum(s-1)
    }
    sum(n)
    return m  
}

func add(a,b int)bool{
    sum ,arr := a^b, a&b
    fmt.Println(sum)
    fmt.Println(arr) 
    return arr > 0 && add(sum,arr << 1)  
}
```
