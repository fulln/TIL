## 编写一个函数来查找字符串数组中的最长公共前缀。
 
```go
package main

//编写一个函数来查找字符串数组中的最长公共前缀。
//
// 如果不存在公共前缀，返回空字符串 ""。
//
// 示例 1:
//
// 输入: ["flower","flow","flight"]
//输出: "fl"
//
//
// 示例 2:
//
// 输入: ["dog","racecar","car"]
//输出: ""
//解释: 输入不存在公共前缀。
//
//
// 说明:
//
// 所有输入只包含小写字母 a-z 。
// Related Topics 字符串
// 👍 1138 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func longestCommonPrefix(strs []string) string {

	var nums []string
	var checked = -1

	if len(strs) > 0 {

		for i := 0; i < len(strs[0]); i++ {
			nums = append(nums, string(strs[0][i]))
		}
		checked = len(nums) - 1

		for i := 1; i < len(strs); i++ {
			cc := -1
			for j := 0; j < len(strs[i]) && j <= checked; j++ {
				if string(strs[i][j]) == nums[j] {
					cc = j
				} else {
					break
				}
			}
			if checked > cc {
				checked = cc
			}
		}
	}
	returns := ""
	if checked == -1 {
		return returns
	}
	for i := 0; i <= checked; i++ {
		returns += nums[i]
	}
	return returns

}

//leetcode submit region end(Prohibit modification and deletion)
func main() {
	var strs = []string{"aca", "cba"}
	prefix := longestCommonPrefix(strs)
	print(prefix)
}
```
