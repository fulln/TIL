## 1175. 质数排列
请你帮忙给从 1 到 n 的数设计排列方案，使得所有的「质数」都应该被放在「质数索引」（索引从 1 开始）上；你需要返回可能的方案总数。

让我们一起来回顾一下「质数」：质数一定是大于 1 的，并且不能用两个小于它的正整数的乘积来表示。

由于答案可能会很大，所以请你返回答案 模 mod 10^9 + 7 之后的结果即可。

 

示例 1：

输入：n = 5
输出：12
解释：举个例子，[1,2,5,4,3] 是一个有效的排列，但 [5,2,3,4,1] 不是，因为在第二种情况里质数 5 被错误地放在索引为 1 的位置上。
示例 2：

输入：n = 100
输出：682289015
 

提示：

1 <= n <= 100

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/prime-arrangements
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func numPrimeArrangements(n int) int {
    p:= 0
    j:= 1
    ans := 1
    ans2 := 1
    mod := 1000000007 
    for i:= 2;i <= n;i++{
        if isPrime(i){
            p++
            ans = ans * p % mod
        }else{
            j++
            ans2= ans2 *j % mod
        }
    }
    return  ans * ans2 % mod
}

func isPrime(n int) bool {
    for i := 2; i*i <= n; i++ {
        if n%i == 0 {
            return false
        }
    }
    return true
}

```
