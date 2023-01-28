## 1664. Ways to Make a Fair Array

You are given an integer array `nums`. You can choose **exactly one** index (**0-indexed**) and remove the element. Notice that the index of the elements may change after the removal.

For example, if `nums = [6,1,7,4,1]`:

-   Choosing to remove index `1` results in `nums = [6,7,4,1]`.
-   Choosing to remove index `2` results in `nums = [6,1,4,1]`.
-   Choosing to remove index `4` results in `nums = [6,1,7,4]`.

An array is **fair** if the sum of the odd-indexed values equals the sum of the even-indexed values.

Return the _**number** of indices that you could choose such that after the removal,_ `nums` _is **fair**._

**Example 1:**

**Input:** nums = [2,1,6,4]
**Output:** 1
**Explanation:**
Remove index 0: [1,6,4] -> Even sum: 1 + 4 = 5. Odd sum: 6. Not fair.
Remove index 1: [2,6,4] -> Even sum: 2 + 4 = 6. Odd sum: 6. Fair.
Remove index 2: [2,1,4] -> Even sum: 2 + 4 = 6. Odd sum: 1. Not fair.
Remove index 3: [2,1,6] -> Even sum: 2 + 6 = 8. Odd sum: 1. Not fair.
There is 1 index that you can remove to make nums fair.

**Example 2:**

**Input:** nums = [1,1,1]
**Output:** 3
**Explanation:** You can remove any index and the remaining array is fair.

**Example 3:**

**Input:** nums = [1,2,3]
**Output:** 0
**Explanation:** You cannot make a fair array after removing any index.

**Constraints:**

-   `1 <= nums.length <= 105`
-   `1 <= nums[i] <= 104`

```GO

func waysToMakeFair(nums []int) int {

// dynamic 就是 2份。0 是包含当前的sum。1 是不包含当前的sum

// 2个数组 1 是奇数和 2 是偶数和。

// 总奇数和 - 当前奇数和 + 当前-1 偶数和

// 总偶数和 - 当前偶数和 + 当前-1 奇数和

// 遍历全部。存在就返回当前index

dp := make([][]int,len(nums))

  

for i := range dp{

dp[i] = make([]int,2)

}

  

dp[0][0] = nums[0]

dp[0][1] = 0

  

for i:=1;i < len(nums); i++{

dp[i][i&1] = dp[i-1][i&1] + nums[i]

dp[i][i&1^1] = dp[i-1][i&1^1]

}


ret := 0

n := len(nums)

for i:= 0;i< len(nums);i++{

if i == 0{

if dp[n-1][0]-dp[i][0] == dp[n-1][1]-dp[i][1]{

ret ++

}

}else{

if dp[n-1][0]-dp[i][0] + dp[i-1][1] == dp[n-1][1]-dp[i][1] + dp[i-1][0]{

ret ++

}

}

}

  

return ret

  

}
```