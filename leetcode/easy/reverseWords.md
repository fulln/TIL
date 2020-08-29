## 反转字符串中的单词 III

给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。

 

示例：

输入："Let's take LeetCode contest"
输出："s'teL ekat edoCteeL tsetnoc"
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-words-in-a-string-iii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func reverseWords(s string) string {
	split := strings.Split(s, " ")
	var returns string
	for _,val := range split {
		for end:= len(val) -1;end >=0 ;end -- {
			//val[from],val[end] = val[end],val[from]
			//
			//val[from] = val[end]
			//val[end]  =val[from]
			returns +=string(val[end])
		}
		returns+=" "
	}
	return strings.Trim(returns," ")
}

```
