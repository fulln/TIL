## 验证回文字符串 Ⅱ

给定一个非空字符串 s，最多删除一个字符。判断是否能成为回文字符串。

示例 1:

输入: "aba"
输出: True
示例 2:

输入: "abca"
输出: True
解释: 你可以删除c字符。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-palindrome-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func validPalindrome(s string) bool {
    for from,end := 0,len(s)-1; from < end ;{
        if s[from] == s[end]{
            from ++
            end --            
        }else{
            flag1, flag2 := true, true
            for i, j := from, end - 1; i < j; i, j = i + 1, j - 1 {
                if s[i] != s[j] {
                    flag1 = false
                    break
                }
            }
            for i, j := from + 1, end; i < j; i, j = i + 1, j - 1 {
                if s[i] != s[j] {
                    flag2 = false
                    break
                }
            }
            return flag1 || flag2
        }
    }

    return true
}

```
