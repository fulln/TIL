## plus_one_加一

```go
package main

//给定一个由整数组成的非空数组所表示的非负整数，在该数的基础上加一。
//
// 最高位数字存放在数组的首位， 数组中每个元素只存储单个数字。
//
// 你可以假设除了整数 0 之外，这个整数不会以零开头。
//
// 示例 1:
//
// 输入: [1,2,3]
//输出: [1,2,4]
//解释: 输入数组表示数字 123。
//
//
// 示例 2:
//
// 输入: [4,3,2,1]
//输出: [4,3,2,2]
//解释: 输入数组表示数字 4321。
//
// Related Topics 数组
// 👍 516 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func plusOne(digits []int) []int {
	//递归
	length := len(digits)

	digits[length-1]++

	if digits[length-1] == 10 {
		digits[length-1] = 0
		if length == 1 {
			return []int{1, 0}
		} else {
			digits = append(plusOne(digits[:length-1]), digits[length-1])
		}
	}
	return digits
}
func main() {
	var dict = []int{9}
	one := plusOne(dict)
	print(one)

}

//leetcode submit region end(Prohibit modification and deletion)

```



