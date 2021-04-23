##  最大整除子集

给你一个由 无重复 正整数组成的集合 nums ，请你找出并返回其中最大的整除子集 answer ，子集中每一元素对 (answer[i], answer[j]) 都应当满足：
answer[i] % answer[j] == 0 ，或
answer[j] % answer[i] == 0
如果存在多个有效解子集，返回其中任何一个均可。

 

示例 1：

输入：nums = [1,2,3]
输出：[1,2]
解释：[1,3] 也会被视为正确答案。
示例 2：

输入：nums = [1,2,4,8]
输出：[1,2,4,8]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/largest-divisible-subset
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


```go
func largestDivisibleSubset(nums []int) []int {
    dp := make([]int,len(nums))
    maxSize :=1
    maxValue:=0
    sort.Ints(nums)
    n := len(nums)
    for i:=0; i<n; i++ {
        dp[i] = 1
    }
    for i:=1;i< n;i++{
        for j :=0;j < i;j++{
            if nums[i] % nums[j] == 0{
                dp[i] = max(dp[i],dp[j] +1)
            }
        }
        if dp[i] >maxSize{
            maxSize = dp[i]
            maxValue = i 
        }
    }
    res := []int{}

    for i:= maxValue ;i>=0;i --{
         if(nums[maxValue] % nums[i] == 0 && dp[i]==maxSize && maxSize >= 0){
                maxValue = i
                res = append(res,nums[i]);
                maxSize--;
        }
    }
    return res



}

func max(a,b int)int{
    if a >b {
        return a
    }else{
        return b
    }
}
```
