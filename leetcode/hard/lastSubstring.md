#字典 #数据结构 #算法  

#### [1163. 按字典序排在最后的子串](https://leetcode.cn/problems/last-substring-in-lexicographical-order/)

给你一个字符串 s ，找出它的所有子串并按字典序排列，返回排在最后的那个子串。

 

示例 1：

输入：s = "abab"
输出："bab"
解释：我们可以找出 7 个子串 ["a", "ab", "aba", "abab", "b", "ba", "bab"]。按字典序排在最后的子串是 "bab"。
示例 2：

输入：s = "leetcode"
输出："tcode"
 

提示：

1 <= s.length <= 4 * 105
s 仅含有小写英文字符。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/last-substring-in-lexicographical-order
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func lastSubstring(s string) string {
	i, n := 0, len(s)
	for j, k := 1, 0; j+k < n; {
		if s[i+k] == s[j+k] {
			k++
		} else if s[i+k] < s[j+k] {
			i += k + 1
			k = 0
			if i >= j {
				j = i + 1
			}
		} else {
			j += k + 1
			k = 0
		}
	}
	return s[i:]
}

作者：lcbin
链接：https://leetcode.cn/problems/last-substring-in-lexicographical-order/solution/python3javacgotypescript-yi-ti-yi-jie-sh-3amj/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```
