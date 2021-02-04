## 搜索旋转排序数组

升序排列的整数数组 nums 在预先未知的某个点上进行了旋转（例如， [0,1,2,4,5,6,7] 经旋转后可能变为 [4,5,6,7,0,1,2] ）。

请你在数组中搜索 target ，如果数组中存在这个目标值，则返回它的索引，否则返回 -1 。

 

示例 1：

输入：nums = [4,5,6,7,0,1,2], target = 0
输出：4
示例 2：

输入：nums = [4,5,6,7,0,1,2], target = 3
输出：-1
示例 3：

输入：nums = [1], target = 0
输出：-1
 

提示：

1 <= nums.length <= 5000
-10^4 <= nums[i] <= 10^4
nums 中的每个值都 独一无二
nums 肯定会在某个点上旋转
-10^4 <= target <= 10^4

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvyz1t/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func search(nums []int, target int) int {
	start := 0
	end := len(nums) - 1


	for start <= end {
		middle := (start + end) / 2
		if nums[middle] == target {
			return middle
		}

		if nums[middle] < target {
			if nums[end] == target {
				return end
			}
			if nums[end] > target {
				start = middle
				continue
			}
			i := search(nums[:middle], target)
			if i == -1 {
				return -1
			} else {
				return start + i
			}
		}

		if nums[middle] > target {
			if nums[start] == target {
				return start
			}
			if nums[start] < target {
				end = middle
				continue
			}
			i := search(nums[middle+1:], target)
			if i == -1 {
				return -1
			} else {
				return middle + i
			}
		}
	}
	return -1
}
```
