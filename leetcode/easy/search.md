## 53 - I. 在排序数组中查找数字 I

统计一个数字在排序数组中出现的次数。

 

示例 1:

输入: nums = [5,7,7,8,8,10], target = 8
输出: 2
示例 2:

输入: nums = [5,7,7,8,8,10], target = 6
输出: 0
 

限制：

0 <= 数组长度 <= 50000

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zai-pai-xu-shu-zu-zhong-cha-zhao-shu-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func search(nums []int, target int) int {
    //2分

    l := len(nums)

    sum :=0
    for i:=0 ;i<l;i++{
        if target == nums[i]{
            sum ++
        }
    }

    return sum

}
```
