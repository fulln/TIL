## 计数质数

统计所有小于非负整数 n 的质数的数量。

 

示例 1：

输入：n = 10
输出：4
解释：小于 10 的质数一共有 4 个, 它们是 2, 3, 5, 7 。
示例 2：

输入：n = 0
输出：0
示例 3：

输入：n = 1
输出：0


```go
func countPrimes(n int) int {

    counts := make([]bool,n)
    s := 0
    for i:=2;i< n;i++{
        if  !counts[i]{
                s++
                for j:=2;i*j < n;j++{
                    counts[j*i] = true
                }
        }
    }

    return s

}
```