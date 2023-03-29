## 1641. 统计字典序元音字符串的数目

给你一个整数 n，请返回长度为 n 、仅由元音 (a, e, i, o, u) 组成且按 字典序排列 的字符串数量。

字符串 s 按 字典序排列 需要满足：对于所有有效的 i，s[i] 在字母表中的位置总是与 s[i+1] 相同或在 s[i+1] 之前。

 

示例 1：

输入：n = 1
输出：5
解释：仅由元音组成的 5 个字典序字符串为 ["a","e","i","o","u"]
示例 2：

输入：n = 2
输出：15
解释：仅由元音组成的 15 个字典序字符串为
["aa","ae","ai","ao","au","ee","ei","eo","eu","ii","io","iu","oo","ou","uu"]
注意，"ea" 不是符合题意的字符串，因为 'e' 在字母表中的位置比 'a' 靠后
示例 3：

输入：n = 33
输出：66045

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/count-sorted-vowel-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func countVowelStrings(n int) int {

   return (n+4)* (n+3) * (n+2) * (n+1)/24

}

// 或者
func countVowelStrings(n int) int {

    dp:= []int{1,1,1,1,1}

    for i:=1;i<n;i++{

        dp[1] += dp[0]

        dp[2] += dp[1] 

        dp[3] += dp[2]

        dp[4] += dp[3]

    }

    return dp[0] +dp[1] +dp[2] +dp[3] +dp[4] 

}


```

