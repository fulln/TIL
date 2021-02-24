## 最长上升子序列

最长上升子序列
给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。

 
示例 1：

输入：nums = [10,9,2,5,3,7,101,18]
输出：4
解释：最长递增子序列是 [2,3,7,101]，因此长度为 4 。
示例 2：

输入：nums = [0,1,0,3,2,3]
输出：4
示例 3：

输入：nums = [7,7,7,7,7,7,7]
输出：1
 

提示：

1 <= nums.length <= 2500
-104 <= nums[i] <= 104
 

进阶：

你可以设计时间复杂度为 O(n2) 的解决方案吗？
你能将算法的时间复杂度降低到 O(n log(n)) 吗?


作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xwhvq3/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
//动态规划
func lengthOfLIS(nums []int) int {
    dp :=make([]int,len(nums))
	//最长的长度就是倒数长度+1
	res := 0
	for i:=0;i< len(nums);i++{
		dp[i] = 1
		for j:=0;j < i;j++{
			if nums[i] <= nums[j] {
				continue
			}else {
				max := dp[j] + 1
				if dp[i] < max{
					dp[i] = max
				}
			}
		}
		if res <dp[i] {
			res =dp[i]
		}
	}
	return res;
}
//2分
func lengthOfLIS(nums []int) int {
	tail := make([]int,len(nums))
	res :=0
	for _,num := range nums{
		i,j := 0,res
		for i<j{
			m := (i+j)/2
			if nums[m] < num {
				i = m+1
			}else{
				j= m
			}
		}
		tail[i] = num
		if j ==res{
			res ++
		}
	}
	return res;
}
```
