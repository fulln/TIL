##  [338. 比特位计数](https://leetcode.cn/problems/counting-bits/)

给你一个整数 n ，对于 0 <= i <= n 中的每个 i ，计算其二进制表示中 1 的个数 ，返回一个长度为 n + 1 的数组 ans 作为答案。

示例 1：

输入：n = 2
输出：[0,1,1]
解释：
0 --> 0
1 --> 1
2 --> 10
示例 2：

输入：n = 5
输出：[0,1,1,2,1,2]
解释：
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101
 

提示：

0 <= n <= 10

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/counting-bits
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func countBits(n int) []int {

  

    dp := make([]int,n+1)

    dp[0] = 0

    last := 0

    for i:= 1;i<=n;i++{

        if i> 1 && i&(i-1) == 0{

            dp[i] = 1

            last = i

            continue

        }

        dp[i] = dp[i -last] + 1

    }

  

    return dp

}
```