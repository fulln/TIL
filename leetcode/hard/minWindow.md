##  最小覆盖子串
给你一个字符串 s 、一个字符串 t 。返回 s 中涵盖 t 所有字符的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 "" 。

 

注意：

对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。
如果 s 中存在这样的子串，我们保证它是唯一的答案。
 

示例 1：

输入：s = "ADOBECODEBANC", t = "ABC"
输出："BANC"
示例 2：

输入：s = "a", t = "a"
输出："a"
示例 3:

输入: s = "a", t = "aa"
输出: ""
解释: t 中两个字符 'a' 均应包含在 s 的子串中，
因此没有符合条件的子字符串，返回空字符串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-window-substring
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func minWindow(s string, t string) string {
    ms := make(map[byte]int)
    mt := make(map[byte]int)
    n := len(s) 
    for i:=0;i<len(t);i++ {
        mt[t[i]]++
    }

    minl := -1

    for left,right :=0,0; right < len(s);right++{
        if mt[s[right]]  > 0{
            ms[s[right]] ++
        }
        for check(ms,mt) && left <= right{
            if right - left  < n{
                n = right - left 
                minl = left
            } 
            if ms[s[left]] > 0 {
                ms[s[left]]--
            }

            left++
        }
    }
    if minl == -1{
        return ""
    } 

    return s[minl:minl + n+1]

}

func check(s,t map[byte]int)bool{
    for key,val := range t{
        if s[key] < val {
            return false
        }
    }
    return true
}
```
