## 两个字符串的删除操作
给定两个单词 word1 和 word2，找到使得 word1 和 word2 相同所需的最小步数，每步可以删除任意一个字符串中的一个字符。

 

示例：

输入: "sea", "eat"
输出: 2
解释: 第一步将"sea"变为"ea"，第二步将"eat"变为"ea"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/delete-operation-for-two-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func minDistance(word1 string, word2 string) int {
    //  1. 确定数组和下标
    dp := make([][]int, len(word1)+1)
	for i := 0; i < len(dp); i++ {
		dp[i] = make([]int, len(word2)+1)
	}
    // 2. 初始化值
    for i:=0;i< len(dp);i++{
        dp[i][0] = i
    }
    for j:=0;j< len(dp[0]);j++{
        dp[0][j] = j
    }

    for i:=1;i <=len(word1);i++{
        for j:=1;j<= len(word2);j++{
            if word1[i-1] == word2[j-1]{
                dp[i][j] = dp[i-1][j-1]
            }else{
                dp[i][j] =min(dp[i-1][j-1]+2, min(dp[i-1][j]+1,dp[i][j-1]+1))
            }
        }
    }
    return dp[len(word1)][len(word2)]

}

func min(a,b int)int{
    if a < b{
        return a
    }else{
        return b
    }
}
```
