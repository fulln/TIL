## 搜索插入位置

```go 
package main

//给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。
//
// 你可以假设数组中无重复元素。
//
// 示例 1:
//
// 输入: [1,3,5,6], 5
//输出: 2
//
//
// 示例 2:
//
// 输入: [1,3,5,6], 2
//输出: 1
//
//
// 示例 3:
//
// 输入: [1,3,5,6], 7
//输出: 4
//
//
// 示例 4:
//
// 输入: [1,3,5,6], 0
//输出: 0
//
// Related Topics 数组 二分查找
// 👍 611 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func searchInsert(nums []int, target int) int {
	var middle int
	for from, end := 0, len(nums)-1; ; {

		middle = from + ((end - from) / 2)

		if nums[middle] > target {
			if middle-1 < 0 {
				return 0
			}
			if nums[middle-1] < target {
				return middle
			} else if nums[middle-1] == target {
				return middle - 1
			}
			end = middle - 1
		} else if nums[middle] < target {
			if middle+1 >= len(nums) {
				return len(nums)
			}
			if nums[middle+1] >= target {
				return middle + 1
			}
			from = middle + 1
		} else {
			return middle
		}
	}

}
func main() {
	var num = []int{123}
	insert := searchInsert(num, 1309)
	print(insert)
}

//leetcode submit region end(Prohibit modification and deletion)
```