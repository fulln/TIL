## 1262. 可被三整除的最大和
给你一个整数数组 nums，请你找出并返回能被三整除的元素最大和。

 

示例 1：

输入：nums = [3,6,5,1,8]
输出：18
解释：选出数字 3, 6, 1 和 8，它们的和是 18（可被 3 整除的最大和）。
示例 2：

输入：nums = [4]
输出：0
解释：4 不能被 3 整除，所以无法选出数字，返回 0。
示例 3：

输入：nums = [1,2,3,4,4]
输出：12
解释：选出数字 1, 3, 4 以及 4，它们的和是 12（可被 3 整除的最大和）。


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/greatest-sum-divisible-by-three
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
const INT_MAX = int(^uint(0) >> 1)
const INT_MIN = ^INT_MAX

func maxSumDivThree(nums []int) int {
    // 动态规划
    dp :=[]int{0,INT_MIN,INT_MIN}

    for _,val := range nums{
        temp := []int{0,0,0}
        for i:=0;i<3;i++{
            temp[(i+val)%3] = max(dp[(i+val)%3],dp[i] +val) 
        }
        dp = temp
    }

    return dp[0]
}

func max(a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}

```
