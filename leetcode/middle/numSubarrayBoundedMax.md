## 区间子数组个数

给定一个元素都是正整数的数组A ，正整数 L 以及 R (L <= R)。

求连续、非空且其中最大元素满足大于等于L 小于等于R的子数组个数。

例如 :
输入: 
A = [2, 1, 4, 3]
L = 2
R = 3
输出: 3
解释: 满足条件的子数组: [2], [2, 1], [3].

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-subarrays-with-bounded-maximum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


```go
func numSubarrayBoundedMax(nums []int, left int, right int) int {
    return counts(nums,right) - counts(nums,left -1)
}

func  counts(nums []int,limit int)int{
    curr,total :=0,0

    for _,val := range nums{
        if val <= limit{
            curr  ++
        }else{
            curr = 0
        }
        total +=curr
    }
    return total
}

```
