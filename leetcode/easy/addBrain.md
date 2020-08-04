## addBrain-2进制计算

```go
package main

import (
	"strconv"
	"strings"
)

// 给你两个二进制字符串，返回它们的和（用二进制表示）。
//
// 输入为 非空 字符串且只包含数字 1 和 0。
//
//
//
// 示例 1:
//
// 输入: a = "11", b = "1"
// 输出: "100"
//
// 示例 2:
//
// 输入: a = "1010", b = "1011"
// 输出: "10101"
//
//
//
// 提示：
//
//
// 每个字符串仅由字符 '0' 或 '1' 组成。
// 1 <= a.length, b.length <= 10^4
// 字符串如果不是 "0" ，就都不含前导零。
//
// Related Topics 数学 字符串
// 👍 444 👎 0

//1. 判断 2个string长度
//2. 倒遍历 长的数组
//3. 将2个值相加，如果大于2 往前+1
// 4. 导出结果
//leetcode submit region begin(Prohibit modification and deletion)

func addBinary(a string, b string) string {
	if len(a) >= len(b) {
		return compare(a, b)
	} else {
		return compare(b, a)
	}
}

func compare(a string, b string) string {
	var zero = []string{"0"}
	var one = []string{"1"}

	lena := len(a)
	added := 0
	var split []string
	lenb := len(b)

	for lena > 0 {
		result, _ := strconv.ParseInt(string(a[lena-1]), 10, 32)
		value := int(result)
		value = value + added
		if lenb > 0 {
			resultb, _ := strconv.ParseInt(string(b[lenb-1]), 10, 32)
			value = value + int(resultb)
		}
		if value == 2 {
			if lena == 1 {
				split = append([]string{"10"}, split...)
				break
			}
			split = append(zero, split...)
			added = 1
		} else if value == 1 {
			split = append(one, split...)
			added = 0
		} else if value == 3 {
			if lena == 1 {
				split = append([]string{"11"}, split...)
				break
			}
			split = append(one, split...)
			added = 1
		} else {
			split = append(zero, split...)
			added = 0
		}
		lena--
		lenb--
	}
	return strings.Join(split, "")

}

func main() {
	a := "1111"
	b := "1111"
	binary := addBinary(a, b)
	print(binary)
}

//leetcode submit region end(Prohibit modification and deletion)

```
