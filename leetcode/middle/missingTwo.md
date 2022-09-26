## 面试题 17.19. 消失的两个数字
给定一个数组，包含从 1 到 N 所有的整数，但其中缺了两个数字。你能在 O(N) 时间内只用 O(1) 的空间找到它们吗？

以任意顺序返回这两个数字均可。

示例 1:

输入: [1]
输出: [2,3]
示例 2:

输入: [2,3]
输出: [1,4]
提示：

nums.length <= 30000


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/missing-two-lcci
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func missingTwo(nums []int) []int {
    sort.Ints(nums)    
    sum := len(nums)+2

    xorSum := 0
    for _, num := range nums {
        xorSum ^= num
    }
    for i := 1; i <= sum; i++ {
        xorSum ^= i
    }

    diff := xorSum & -xorSum
    a := 0
	for _, v := range nums {
		if (v & diff) != 0 {
			a ^= v
		}
	}
	for i := 1; i <= sum; i++ {
		if (i & diff) != 0 {
			a ^= i
		}
	}    
    return []int{a,xorSum^a}
}

```
