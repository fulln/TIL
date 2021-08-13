## 数字 1 的个数
给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。

 

示例 1：

输入：n = 13
输出：6
示例 2：

输入：n = 0
输出：0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-digit-one
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
// 暴力解法 超时
func countDigitOne(n int) int {
	f := make([]int, n+1)
	f[0] = 0
	ans := 0
	for i := 1; i <= n; i++ {
		j := i / 10
		count := 0
		if i%10 == 1 {
			count = 1
		}
		f[i] = f[j] + count
		ans += f[i]
	}
	return ans
}
```
