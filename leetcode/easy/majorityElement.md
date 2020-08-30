##  多数元素

给定一个大小为 n 的数组，找到其中的多数元素。多数元素是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/majority-element
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//空间最大O(n)
//最大时间O(n)
func majorityElement(nums []int) int {
	times  := map[int]int{}
	for _,val := range nums {
		times[val]++
	}
	current := nums[0]
	for key,val := range times{
		if times[current] < val{
			current = key
		}
	}
	return  current
}
//摩尔投票法
//时间最大O(n)
//空间 O(1)
func majorityElement(nums []int) int {
	index := 0
	curent := 0

	for _,val := range nums{

		if index == 0{
			curent = val

		}

		if curent == val {
			index ++
		}else{
			index --
		}


	}
	return curent
}


```
