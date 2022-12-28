## 最大平均值和的分组
给定数组 nums 和一个整数 k 。我们将给定的数组 nums 分成 最多 k 个相邻的非空子数组 。 分数 由每个子数组内的平均值的总和构成。

注意我们必须使用 nums 数组中的每一个数进行分组，并且分数不一定需要是整数。

返回我们所能得到的最大 分数 是多少。答案误差在 10-6 内被视为是正确的。

 

示例 1:

输入: nums = [9,1,2,3,9], k = 3
输出: 20.00000
解释: 
nums 的最优分组是[9], [1, 2, 3], [9]. 得到的分数是 9 + (1 + 2 + 3) / 3 + 9 = 20. 
我们也可以把 nums 分成[9, 1], [2], [3, 9]. 
这样的分组得到的分数为 5 + 2 + 6 = 13, 但不是最大值.
示例 2:

输入: nums = [1,2,3,4,5,6,7], k = 4
输出: 20.50000
 

提示:

1 <= nums.length <= 100
1 <= nums[i] <= 104
1 <= k <= nums.length

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/largest-sum-of-averages
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func largestSumOfAverages(nums []int, k int) float64 {
    n := len(nums)
    sums := make([]float64,n+1)
    for i:=0;i < n;i++{
        sums[i+1] = sums[i] + float64(nums[i])
    }

    dp := make([][]float64,n+1)

    for i:= 1;i<= n;i++{
        dp[i] =  make([]float64,n+1)
        dp[i][1] =sums[i] / float64(i)
    }

    
    for j :=2;j <= k;j++{
        for  i:=j;i <= n;i++{
            for m :=j-1;m < i;m++{
                dp[i][j] = math.Max(dp[i][j],dp[m][j-1]+   (sums[i] - sums[m])/float64(i-m))
            }             
        }
    }

    return dp[n][k]


}

```
