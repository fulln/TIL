## 剑指 Offer 21. 调整数组顺序使奇数位于偶数前面

输入一个整数数组，实现一个函数来调整该数组中数字的顺序，使得所有奇数位于数组的前半部分，所有偶数位于数组的后半部分。

 

示例：

输入：nums = [1,2,3,4]
输出：[1,3,2,4] 
注：[3,1,2,4] 也是正确的答案之一。
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/diao-zheng-shu-zu-shun-xu-shi-qi-shu-wei-yu-ou-shu-qian-mian-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func exchange(nums []int) []int {
	returns := []int{}
	return2 := []int{}
	begin1,begin2 := 0,0

	for _,val :=range nums{
		if val & 1 == 1{
			returns = append(returns,val)
			begin1 ++
		}else{
			return2 = append(return2,val)
			begin2 ++
		}
	}
	return append(returns,return2...)
}
func exchange(nums []int) []int {

	//O(1)
	q,all := 0,0
	for _,val :=range nums{
		if val & 1 == 1{
			nums[q],nums[all] = nums[all],nums[q]
			q++
		}
		all ++
	}
	return nums
}

```
