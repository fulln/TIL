## 单词拆分

给定一个非空字符串 s 和一个包含非空单词的列表 wordDict，判定 s 是否可以被空格拆分为一个或多个在字典中出现的单词。

说明：

拆分时可以重复使用字典中的单词。
你可以假设字典中没有重复的单词。
示例 1：

输入: s = "leetcode", wordDict = ["leet", "code"]
输出: true
解释: 返回 true 因为 "leetcode" 可以被拆分成 "leet code"。
示例 2：

输入: s = "applepenapple", wordDict = ["apple", "pen"]
输出: true
解释: 返回 true 因为 "applepenapple" 可以被拆分成 "apple pen apple"。
     注意你可以重复使用字典中的单词。
示例 3：

输入: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
输出: false

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/xa503c/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func wordBreak(s string, wordDict []string) bool {
    dp := make([]bool,len(s)+1)
    dp[0]=true
    for i:=1; i<= len(s);i++{
        for j:=0;j<i;j++{
            if dp[j] && contains(s[j:i],wordDict){
                dp[i]=true
                break
            }
        }
    }
    return dp[len(s)]

}

func contains(s string,dict []string)bool{
    for _,val:= range dict{
        if val == s{
            return true
        }
    }
    return false
}
```
