##  连续数组
给定一个二进制数组, 找到含有相同数量的 0 和 1 的最长连续子数组（的长度）。

 

示例 1:

输入: [0,1]
输出: 2
说明: [0, 1] 是具有相同数量0和1的最长连续子数组。
示例 2:

输入: [0,1,0]
输出: 2
说明: [0, 1] (或 [1, 0]) 是具有相同数量0和1的最长连续子数组。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/contiguous-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func findMaxLength(nums []int) int {
    for  i:=0;i< len(nums);i++{
        if nums[i] ==0{
            nums[i] =-1
        }
    }
    maps := make(map[int]int)
    sum := 0
    curr := 0
    for i:=0;i<len(nums);i++{
        sum += nums[i]
        if sum == 0 && i > curr{
            curr = i +1
        }

        if val,ok := maps[sum];ok{
            curr = max(i - val,curr)
        }else{
            maps[sum] = i
        }
    }
    
    return curr

}

func max (a,b int)int{
    if a> b{
        return a
    }else{
        return b
    }
}
```
