## 最长回文子序列

给你一个字符串 s ，找出其中最长的回文子序列，并返回该序列的长度。

子序列定义为：不改变剩余字符顺序的情况下，删除某些字符或者不删除任何字符形成的一个序列。

 

示例 1：

输入：s = "bbbab"
输出：4
解释：一个可能的最长回文子序列为 "bbbb" 。
示例 2：

输入：s = "cbbd"
输出：2
解释：一个可能的最长回文子序列为 "bb" 。
 

提示：

1 <= s.length <= 1000
s 仅由小写英文字母组成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-palindromic-subsequence
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func longestPalindromeSubseq(s string) int {

    dp := make([][]int,len(s))
    for i,_ := range dp{
        dp[i] = make([]int,len(s))
    }

    for i:= len(s) -1;i >= 0;i--{
        dp[i][i] =1
        for j :=i+1;j <len(s);j++{
            if s[i] == s[j]{
                dp[i][j] = dp[i+1][j-1]+2 
            }else{
                dp[i][j] = max(dp[i+1][j],dp[i][j-1])
            }
        }
    }
    return dp[0][len(s)-1]


}
func max(a,b int)int{

    if a > b{
        return a
    }else{
        return b
    }
}
```
