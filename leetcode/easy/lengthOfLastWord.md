
## lengthOfLastWord-最后一个单词

```go
//给定一个仅包含大小写字母和空格 ' ' 的字符串 s，返回其最后一个单词的长度。如果字符串从左向右滚动显示，那么最后一个单词就是最后出现的单词。
//
// 如果不存在最后一个单词，请返回 0 。
//
// 说明：一个单词是指仅由字母组成、不包含任何空格字符的 最大子字符串。
//
//
//
// 示例:
//
// 输入: "Hello World"
//输出: 5
//
// Related Topics 字符串
// 👍 225 👎 0


//leetcode submit region begin(Prohibit modification and deletion)
func lengthOfLastWord(s string) int {
	//分治
	index := len(s) /2
	for{
		 if string(s[index]) == ""{
			index = index + index/2
		}

	}

	return 0
}
func main() {
	lengthOfLastWord("Hello World")
}
//leetcode submit region end(Prohibit modification and deletion)
```

