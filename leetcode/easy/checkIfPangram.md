## 1832. 判断句子是否为全字母句

全字母句 指包含英语字母表中每个字母至少一次的句子。

给你一个仅由小写英文字母组成的字符串 sentence ，请你判断 sentence 是否为 全字母句 。

如果是，返回 true ；否则，返回 false 。

 

示例 1：

输入：sentence = "thequickbrownfoxjumpsoverthelazydog"
输出：true
解释：sentence 包含英语字母表中每个字母至少一次。
示例 2：

输入：sentence = "leetcode"
输出：false
 



来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/check-if-the-sentence-is-pangram
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func checkIfPangram(sentence string) bool {
    sum := 0
    
    for _,val := range sentence {
        sum |=  1 << (val -'a')
    }

    return sum == (1 << 26) -1 

}
```
