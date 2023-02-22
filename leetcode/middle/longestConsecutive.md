## 最长连续序列
给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

 

进阶：你可以设计并实现时间复杂度为 O(n) 的解决方案吗？

 

示例 1：

输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
示例 2：

输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
 

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/x2xmre/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func longestConsecutive(nums []int) int {
	maps := make(map[int]bool)
	for _,val := range nums{
		maps[val]= true
	}
	ret := 0
	for _,val := range nums{
		if !maps[val-1]{
			temp := val
			current := 1
			for maps[temp + 1] {
				temp ++
				current ++
			}
			if current > ret {
				ret = current
			}
		}
	}
	return ret
}
```
