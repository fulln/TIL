## 数组中的 k-diff 数对
给你一个整数数组 nums 和一个整数 k，请你在数组中找出 不同的 k-diff 数对，并返回不同的 k-diff 数对 的数目。

k-diff 数对定义为一个整数对 (nums[i], nums[j]) ，并满足下述全部条件：

0 <= i, j < nums.length
i != j
nums[i] - nums[j] == k
注意，|val| 表示 val 的绝对值。

 

示例 1：

输入：nums = [3, 1, 4, 1, 5], k = 2
输出：2
解释：数组中有两个 2-diff 数对, (1, 3) 和 (3, 5)。
尽管数组中有两个 1 ，但我们只应返回不同的数对的数量。
示例 2：

输入：nums = [1, 2, 3, 4, 5], k = 1
输出：4
解释：数组中有四个 1-diff 数对, (1, 2), (2, 3), (3, 4) 和 (4, 5) 。
示例 3：

输入：nums = [1, 3, 1, 5, 4], k = 0
输出：1
解释：数组中只有一个 0-diff 数对，(1, 1) 。
 

提示：

1 <= nums.length <= 104
-107 <= nums[i] <= 107
0 <= k <= 107

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/k-diff-pairs-in-an-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func findPairs(nums []int, k int) int {
    sort.Ints(nums)
    n := len(nums)
    sum := 0 
    last := 10000001
    for from,end := 0,1;from < n-1  ; {      
        end = min(n-1,end)
        if nums[end] - nums[from] == k{             
             if last != nums[end]{
                 sum ++
                 last = nums[end]
             }
             from ++
             end ++
        }else if nums[end] - nums[from] < k{
            end ++
            if end > n-1{
                end = n -1
                from ++
            }
        }else{
            from ++
            if from == end{
                end ++
            }
        }
    }
    return sum
}

func min(a,b int)int{
    if a  < b{
        return a
    }else{
        return b
    }
}
```
