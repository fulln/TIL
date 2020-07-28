## 判断一个整数是否是回文数

```go
//回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。
//
// 示例 1:
//
// 输入: 121
//输出: true
//
//
// 示例 2:
//
// 输入: -121
//输出: false
//解释: 从左向右读, 为 -121 。 从右向左读, 为 121- 。因此它不是一个回文数。
//
//
// 示例 3:
//
// 输入: 10
//输出: false
//解释: 从右向左读, 为 01 。因此它不是一个回文数。
//
//
// 进阶:
//
// 你能不将整数转为字符串来解决这个问题吗？
// Related Topics 数学
// 👍 1137 👎 0

//leetcode submit region begin(Prohibit modification and deletion)

package main

import "strconv"

func isPalindrome(x int) bool {
	back := 0
	begin := x
	for {
		if x < 0 {
			return false
		}

		if x == 0 {
			return back == begin
		}

		back = back*10 + x%10
		x = x / 10
	}

}

//leetcode submit region end(Prohibit modification and deletion)

func isPalindrome2(x int) bool {

	begin := strconv.Itoa(x)
	runes := []rune(begin)
	for from, to := 0, len(begin)-1; from < to; from, to = from+1, to-1 {
		runes[from], runes[to] = runes[to], runes[from]
	}

	return begin == string(runes)
	//var end = ""
	//for i := len(begin) -1;i >=0 ;i--  {
	//	end  = end + string(begin[i])
	//}
}
func main() {
	palindrome := isPalindrome2(112211)
	print(palindrome)
}
```

