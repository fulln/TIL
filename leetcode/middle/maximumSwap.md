##  最大交换
给定一个非负整数，你至多可以交换一次数字中的任意两位。返回你能得到的最大值。

示例 1 :

输入: 2736
输出: 7236
解释: 交换数字2和数字7。
示例 2 :

输入: 9973
输出: 9973
解释: 不需要交换。
注意:

给定数字的范围是 [0, 108]

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-swap
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func maximumSwap(num int) int {
	s := strconv.Itoa(num)
	str := []byte(s)
	l := len(str) - 1
	for i := range str {
		temp := str[i]
		index := i
		for j := l; j >= i+1; j-- {
			if str[j] > temp {
				temp = str[j]
				index = j
			}
		}
		if index != i {
			str[i], str[index] = str[index], str[i]
			break
		}
	}
	n, _ := strconv.Atoi(string(str))
	return n
}

```
