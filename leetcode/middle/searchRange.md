## 在排序数组中查找元素的第一个和最后一个位置

给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。

如果数组中不存在目标值 target，返回 [-1, -1]。

进阶：

你可以设计并实现时间复杂度为 O(log n) 的算法解决此问题吗？
 

示例 1：

输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
示例 2：

输入：nums = [5,7,7,8,8,10], target = 6
输出：[-1,-1]
示例 3：

输入：nums = [], target = 0
输出：[-1,-1]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xv4bbv/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func searchRange(nums []int, target int) []int {
    start,end:= 0,len(nums) -1
    returns := []int{-1,-1}
    for start <= end {
        middle := (start+end)/2
        if nums[middle] <target{
            start = middle+1
            continue
        }else if nums[middle] > target{
             end = middle -1
            continue
        }else{
            returns[0] = middle
            returns[1] = middle
            curr := middle -1 
            for start <= curr{
                if nums[curr] == target{
                    returns[0] = curr
                    curr --
                    continue
                }else{
                    break
                }
            }
            curr = middle + 1 
            for end >= curr{
                if nums[curr] == target{
                    returns[1] = curr
                    curr++
                    continue
                }else{
                    break
                }
            }
            return returns
        }
    }
    return returns
}
```
