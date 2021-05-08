## 全排列 II
给定一个可包含重复数字的序列 nums ，按任意顺序 返回所有不重复的全排列。

 

示例 1：

输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]
示例 2：

输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
 

提示：

1 <= nums.length <= 8
-10 <= nums[i] <= 10
```go
func permuteUnique(nums []int) [][]int {
	var result [][]int
	visited := make([]bool, len(nums))
	path := make([]int,0,0)
	// 排序保证后续的剪枝
	sort.Ints(nums)
	dfs(&result, nums, visited, &path)
	return result
}
func dfs(result *[][]int, nums []int, visited []bool, path *[]int) {
	// path的长度 等于 nums元素的个数，将path复制到result中
	if len(*path) == len(nums) {
		temp := make([]int, len(nums), len(nums))
		copy(temp,*path)
		*result = append(*result, temp)
		return
	}
	for i := 0; i < len(nums); i++ {
		// 如果nums的元素被标记为true，证明已经被使用了，需要跳过
		if visited[i] {
			continue
		}
		// 剪枝，保证nums的中相同的元素按顺序组合，就可以避免重复
		if i > 0 && nums[i] == nums[i-1] && visited[i-1] {
			continue
		}
		// 添加至path，更改visited的bool值
		*path = append(*path, nums[i])
		visited[i] = true
		// 递归
		dfs(result, nums, visited, path)
		// 回退
		visited[i] = false
		*path=(*path)[:len(*path)-1]
	}
}
```
