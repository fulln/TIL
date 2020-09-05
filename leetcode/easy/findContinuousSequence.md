##  和为s的连续正数序列
 输入一个正整数 target ，输出所有和为 target 的连续正整数序列（至少含有两个数）。

序列内的数字由小到大排列，不同序列按照首个数字从小到大排列。

 

示例 1：

输入：target = 9
输出：[[2,3,4],[4,5]]
示例 2：

输入：target = 15
输出：[[1,2,3,4,5],[4,5,6],[7,8]]
 

限制：

1 <= target <= 10^5
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/he-wei-sde-lian-xu-zheng-shu-xu-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//自己写的暴力破解法
func findContinuousSequence(target int) [][]int {
	current :=0

	ints := [][]int{}

	currents := []int{}

	for i:= 1 ; i<= target ; i++{

		current += i
		currents = append(currents,i)

		for {
			if  current > target{
				current = current - currents[0]
				currents = currents[1:]
			}
			if current ==  target  {
				if len(currents) > 1{
					ints = append(ints,currents)
				}
				break
			}
			if current <  target{
				break
			}
		}
	}
	return ints
}

// 使用等差数列公式

func findContinuousSequence(target int) [][]int {

	left :=1
	right :=2
	var res [][]int
	for left<right{
		sum :=(left+right)*(right-left+1)/2
		if sum==target{
			var list []int
			for i:=left;i<=right;i++{
				list = append(list,i)
			}
			res = append(res,list)
			left++
		}else if sum<target{
			right++
		}else {
			left++
		}
	}
	return res
}
```
