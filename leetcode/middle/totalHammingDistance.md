## 汉明距离总和

两个整数的 汉明距离 指的是这两个数字的二进制数对应位不同的数量。

计算一个数组中，任意两个数之间汉明距离的总和。

示例:

输入: 4, 14, 2

输出: 6

解释: 在二进制表示中，4表示为0100，14表示为1110，2表示为0010。（这样表示是为了体现后四位之间关系）
所以答案为：
HammingDistance(4, 14) + HammingDistance(4, 2) + HammingDistance(14, 2) = 2 + 2 + 2 = 6.
注意:

数组中元素的范围为从 0到 10^9。
数组的长度不超过 10^4。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/total-hamming-distance
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func totalHammingDistance(nums []int) int {
    ans := 0
	// 由于数组中最大值为1e9,也就是说用31位二进制就能表示最大值了。 
	// 			(x位2进制 可以表示的原码最大值为 2^x-1)
	for i := 0; i < 31; i++ {
		count := [2]int{} // 类似哈希结构，count[0]表示0有多少个，count[1]表示1有多少个
		for t := 0; t < len(nums); t++ {
			count[nums[t]&1]++
			nums[t] >>= 1
		}
		ans += count[0] * count[1]
	}
	return ans
}
```
