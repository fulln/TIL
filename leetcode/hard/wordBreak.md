## 单词拆分 II

给定一个字符串 s 和一个字符串字典 wordDict ，在字符串 s 中增加空格来构建一个句子，使得句子中所有的单词都在词典中。以任意顺序 返回所有这些可能的句子。

注意：词典中的同一个单词可能在分段中被重复使用多次。

 

示例 1：

输入:s = "catsanddog", wordDict = ["cat","cats","and","sand","dog"]
输出:["cats and dog","cat sand dog"]
示例 2：

输入:s = "pineapplepenapple", wordDict = ["apple","pen","applepen","pine","pineapple"]
输出:["pine apple pen apple","pineapple pen apple","pine applepen apple"]
解释: 注意你可以重复使用字典中的单词。
示例 3：

输入:s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
输出:[]


作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/xa9v8i/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```go

func wordBreak(s string, wordDict []string) []string {
	dp := make([][]string, len(s) + 1) 
	dp[0] = []string{""}
	for i := 1; i < len(dp); i++ {
		for j := range wordDict {
			word := wordDict[j]
			wLen := len(word)
			if i < wLen {
				continue
			}
			if s[i - wLen : i] == word {
				for k := range dp[i - wLen] {
					tmp := word
					if dp[i - wLen][k] != "" {
						tmp = dp[i - wLen][k] + " " + word
					}
					dp[i] = append(dp[i], tmp)
				}
			}
		}
	}
	return dp[len(dp) - 1]
}

```
