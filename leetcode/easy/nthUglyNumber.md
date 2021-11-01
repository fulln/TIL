## 丑数 II

给你一个整数 n ，请你找出并返回第 n 个 丑数 。

丑数 就是只包含质因数 2、3 和/或 5 的正整数。

 

示例 1：

输入：n = 10
输出：12
解释：[1, 2, 3, 4, 5, 6, 8, 9, 10, 12] 是由前 10 个丑数组成的序列。
示例 2：

输入：n = 1
输出：1
解释：1 通常被视为丑数

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ugly-number-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func nthUglyNumber(n int) int {
    if n == 0 {
        panic(errors.New("invalid n"))
    }
    m2, m3, m5 := 0, 0, 0
    dp := make([]int, n)
    dp[0] = 1
    for i := 1; i < n; i++ {
        a, b, c := dp[m2]*2, dp[m3]*3, dp[m5]*5
        dp[i] = min(a, min(b, c))
        if dp[i] == a {
            m2++
        }
        if dp[i] == b {
            m3++
        }
        if dp[i] == c {
            m5++
        }
    }
    return dp[n-1]
}

func min(x, y int) int {
    if x < y {
        return x
    }
    return y
}
```
