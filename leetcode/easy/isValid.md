## 判断字符串是否有效

```go
package main


import (
	"strings"
)

//给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
//
// 有效字符串需满足：
//
//
// 左括号必须用相同类型的右括号闭合。
// 左括号必须以正确的顺序闭合。
//
//
// 注意空字符串可被认为是有效字符串。
//
// 示例 1:
//
// 输入: "()"
//输出: true
//
//
// 示例 2:
//
// 输入: "()[]{}"
//输出: true
//
//
// 示例 3:
//
// 输入: "(]"
//输出: false
//
//
// 示例 4:
//
// 输入: "([)]"
//输出: false
//
//
// 示例 5:
//
// 输入: "{[]}"
//输出: true
// Related Topics 栈 字符串
// 👍 1673 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func isValid(s string) bool {
	sum := float64(rune(s[0]))
	for i := 0; i < len(s)-1; i++ {
		a := float64(rune(s[i]))
		b := float64(rune(s[i+1]))
		if a-b < 0 && a-b >= -2 {
			sum = sum - a - b
		} else if a-b > 0 {
			sum = sum - a + b
		} else {
			sum = sum + a + b
		}
	}

	return sum <= float64(len(s)) && sum >= -float64(len(s))
}

func isValid2(s string) bool {
	brackets := []string{"{}", "()", "[]"}
	if s == "" {
		return true
	}
	if len(s)%2 != 0 {
		return false
	}
	times := len(s) / 2
	for i := 0; i < times; i++ {
		for _, v := range brackets {
			for strings.Contains(s, v) {
				s = strings.ReplaceAll(s, v, "")
			}
		}
		if s == "" {
			return true
		}
	}
	return false
}

func main() {
	valid := isValid2("(())")
	print(valid)
}

//leetcode submit region end(Prohibit modification and deletion)
```