## 只出现一次的数字

给定一个非空整数数组，除了某个元素只出现一次以外，其余每个元素均出现两次。找出那个只出现了一次的元素。

说明：

你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？


```go
func singleNumber(nums []int) int {
    //如何体现只出现了2次
    //1. 设置index 和 current
    //2. 循环数组  找到就切掉 index 和 current 并让index++
    //3.找不到就返回nums[index]   
    for index:=1;index <= len(nums) -1;{
        if nums[index] == nums[0]{         
            nums  = append(nums[:index], nums[index+1:]...)
            nums  = nums[1:]
            index = 1
            continue
        }
         index++
    }
    return nums[0]
}
```
