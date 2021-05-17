## 两数相除
给定两个整数，被除数 dividend 和除数 divisor。将两数相除，要求不使用乘法、除法和 mod 运算符。

返回被除数 dividend 除以除数 divisor 得到的商。

整数除法的结果应当截去（truncate）其小数部分，例如：truncate(8.345) = 8 以及 truncate(-2.7335) = -2

 

示例 1:

输入: dividend = 10, divisor = 3
输出: 3
解释: 10/3 = truncate(3.33333..) = truncate(3) = 3
示例 2:

输入: dividend = 7, divisor = -3
输出: -2
解释: 7/-3 = truncate(-2.33333..) = -2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/divide-two-integers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func divide(dividend int, divisor int) int {
	// 注意越界问题
	if divisor == -1 && dividend == -(math.MaxInt32+1) {
		return math.MaxInt32
	}
	dividendAbs := int(math.Abs(float64(dividend)))
	divisorAbs := int(math.Abs(float64(divisor)))
	result := div(dividendAbs, divisorAbs)
	// 还原其本来正负
	if (dividend <= 0 && divisor > 0) || (dividend >= 0 && divisor < 0) {
		return -result
	}
	return result
}

func div(dividend int, divisor int) int {
	result := 0
	for dividend >= divisor {
		multi := 1
		for multi * divisor <= (dividend >> 1) {
			multi <<= 1
		}
		result += multi
		// 相减的结果进入下次循环
		dividend -= multi*divisor
	}
	return result
}

```
