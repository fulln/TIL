## 数组中重复的数字

找出数组中重复的数字。


在一个长度为 n 的数组 nums 里的所有数字都在 0～n-1 的范围内。数组中某些数字是重复的，但不知道有几个数字重复了，也不知道每个数字重复了几次。请找出数组中任意一个重复的数字。

示例 1：

输入：
[2, 3, 1, 0, 2, 5, 3]
输出：2 或 3 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/shu-zu-zhong-zhong-fu-de-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
//时间复杂度最低
func findRepeatNumber(nums []int) int {
    maps := map[int]int{}
    for _,val := range(nums){
        if maps[val] != 0{
            return val
        }else{
            maps[val] =1
        }
    }
    return 0
}
//空间复杂度O(1)
func findRepeatNumber(nums []int) int {
	for i:=0;i< len(nums);i++{
		for j:=0; j< len(nums) -1-i;j++{
			if nums[j] == nums[j+1]{
				return nums[j]
			}else if nums[j] > nums[j+1]{
				nums[j],nums[j+1] = nums[j+1],nums[j]
			}
		}
	}
	return 0
}

```
