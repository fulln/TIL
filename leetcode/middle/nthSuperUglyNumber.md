## 超级丑数

> 最近写代码很无力.对屏幕发呆常有的事情....然后在力扣上面发现有人感受和我其实差不多
> 做的多了，反而觉得自己脑子麻了，脑子都不愿动了
> 太真实了,希望努力调整心态

编写一段程序来查找第 n 个超级丑数。

超级丑数是指其所有质因数都是长度为 k 的质数列表 primes 中的正整数。

示例:

输入: n = 12, primes = [2,7,13,19]
输出: 32 
解释: 给定长度为 4 的质数列表 primes = [2,7,13,19]，前 12 个超级丑数序列为：[1,2,4,7,8,13,14,16,19,26,28,32] 。
说明:

1 是任何给定 primes 的超级丑数。
 给定 primes 中的数字以升序排列。
0 < k ≤ 100, 0 < n ≤ 106, 0 < primes[i] < 1000 。
第 n 个超级丑数确保在 32 位有符整数范围内。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/super-ugly-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func nthSuperUglyNumber(n int, primes []int) int {
    dp := []int{1}
    position := make([]int, len(primes))    //记录每个质数的指针位置

    for len(dp) < n {
        min := minVal(dp, primes, position)    //每次挑选出最小的
        if dp[len(dp)-1] < min {           //防止重复值的情况
            dp = append(dp, min)
        }
    }
    return dp[n-1]
}

func minVal(dp, primes, position []int) int {  //返回最小值，并把相应的指针后移
    min_i, min_val := 0, math.MaxInt32
    for i, prime := range primes {
        if val := dp[position[i]]*prime; val < min_val {
            min_i, min_val = i, val
        }
    }
    position[min_i]++
    return min_val
}
```
