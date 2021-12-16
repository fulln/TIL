## . 有序数组中的单一元素
给你一个仅由整数组成的有序数组，其中每个元素都会出现两次，唯有一个数只会出现一次。

请你找出并返回只出现一次的那个数。

你设计的解决方案必须满足 O(log n) 时间复杂度和 O(1) 空间复杂度。

 

示例 1:

输入: nums = [1,1,2,3,3,4,4,8,8]
输出: 2
示例 2:

输入: nums =  [3,3,7,7,10,11,11]
输出: 10

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/single-element-in-a-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func singleNonDuplicate(nums []int) int {

    left,right := 0,len(nums)-1

    for left < right{
        middle := (left + right) /2

        if  nums[middle] == nums[middle-1]{
            if (middle-left)%2 == 0{
                  right = middle - 2  
            }else{
                  left = middle + 1
            }
        }else if nums[middle] == nums[middle+1]{
            if (right-middle)%2 == 0{
                left = middle + 2
            }else {
                right = middle -1
            }
        }else{
            return nums[middle]
        }
    }
    
    return nums[left]


}
```
