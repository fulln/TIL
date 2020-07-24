## 两数之合

```go
package main

import "fmt"

//给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
//
// 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
//
//
//
// 示例:
//
// 给定 nums = [2, 7, 11, 15], target = 9
//
//因为 nums[0] + nums[1] = 2 + 7 = 9
//所以返回 [0, 1]
//
// Related Topics 数组 哈希表
// 👍 8589 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func twoSum(nums []int, target int) []int {
	var names []int
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if nums[i]+nums[j] == target {
				return append(names, i, j)
			}
		}
	}
	return nil
}

func main() {
	var names = []int{1, 2, 3, 4, 5, 7}
	var sum = twoSum(names, 8)
	fmt.Printf("输出结果为 %d", sum)
}

//leetcode submit region end(Prohibit modification and deletion)
```