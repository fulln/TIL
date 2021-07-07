## 字符串的排列
给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的排列。

换句话说，第一个字符串的排列之一是第二个字符串的 子串 。

 

示例 1：

输入: s1 = "ab" s2 = "eidbaooo"
输出: True
解释: s2 包含 s1 的排列之一 ("ba").
示例 2：

输入: s1= "ab" s2 = "eidboaoo"
输出: False

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/permutation-in-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func checkInclusion(s1 string, s2 string) bool {

   m1, m2 := len(s1), len(s2)
    if m1 > m2 {
        return false
    }
    var map1, map2 [26]int
    for i, val := range s1 {
        map1[val-'a']++
        map2[s2[i]-'a']++
    }
    if map1 == map2 {
        return true
    }
    for i := m1; i < m2; i++ {
        map2[s2[i]-'a']++
        map2[s2[i-m1]-'a']--
        if map1 == map2 {
            return true
        }
    }
    return false

}
```
