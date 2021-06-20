## 子序列宽度之和
// 数学题

给定一个整数数组 A ，考虑 A 的所有非空子序列。

对于任意序列 S ，设 S 的宽度是 S 的最大元素和最小元素的差。

返回 A 的所有子序列的宽度之和。

由于答案可能非常大，请返回答案模 10^9+7。

 
 
 ```go
 func sumSubseqWidths(nums []int) int {
    sort.Ints(nums)
    var mod int64 = 1000000007
    var sum int64
    res := make([]int64,len(nums))
    res[0] =1
    for i:=1;i< len(nums);i++{
            res[i] = res[i-1] * 2 % mod
    }
    for j := 0;j< len(res);j++{
        sum = (sum + (res[j] - res[len(nums)-j-1]) * int64(nums[j])) % mod
    }
    
    return int(sum)

}
 ```
