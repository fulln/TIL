## 最美子字符串的数目

如果某个字符串中 至多一个 字母出现 奇数 次，则称其为 最美 字符串。

例如，"ccjjc" 和 "abab" 都是最美字符串，但 "ab" 不是。
给你一个字符串 word ，该字符串由前十个小写英文字母组成（'a' 到 'j'）。请你返回 word 中 最美非空子字符串 的数目。如果同样的子字符串在 word 中出现多次，那么应当对 每次出现 分别计数。

子字符串 是字符串中的一个连续字符序列。

 

示例 1：

输入：word = "aba"
输出：4
解释：4 个最美子字符串如下所示：
- "aba" -> "a"
- "aba" -> "b"
- "aba" -> "a"
- "aba" -> "aba"
示例 2：

输入：word = "aabb"
输出：9
解释：9 个最美子字符串如下所示：
- "aabb" -> "a"
- "aabb" -> "aa"
- "aabb" -> "aab"
- "aabb" -> "aabb"
- "aabb" -> "a"
- "aabb" -> "abb"
- "aabb" -> "b"
- "aabb" -> "bb"
- "aabb" -> "b"
示例 3：

输入：word = "he"
输出：2
解释：2 个最美子字符串如下所示：
- "he" -> "h"
- "he" -> "e"
 



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-wonderful-substrings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func wonderfulSubstrings(word string) int64 {
    ans := [1024]int{1}
    longs,counts :=0,0
    for _,val := range word{
        longs ^= 1 << (val - 'a') // 计算当前前缀和        
        counts += ans[longs]
        for i:=1 ;i< 1024;i <<= 1{
            counts += ans[longs^i]
        }
        ans[longs]++
    }
    return int64(counts)

}
```
