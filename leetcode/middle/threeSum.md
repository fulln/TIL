## 三数之和

给你一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。

注意：答案中不可以包含重复的三元组。

 

示例：

给定数组 nums = [-1, 0, 1, 2, -1, -4]，

满足要求的三元组集合为：
[
  [-1, 0, 1],
  [-1, -1, 2]
]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvpj16/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


```go
func threeSum(nums []int) [][]int {

    returns := [][]int{}

    if len(nums) < 3 {
		return returns
	}

    
    sort.Ints(nums)
    var sum  int

    for j := 0 ; j < len(nums) ;j++ {

        if nums[j] > 0 {
            break
        }

        if  j > 0 && nums[j] == nums[j -1] {
            continue
        }

        for from ,to := j+1 ,len(nums) -1; from < to;{
            sum = nums[from] + nums[to] + nums[j]
            if sum < 0{
                    from++
            }else if sum > 0{
                    to--
            }else if sum == 0{
                temp := []int{nums[j] , nums[from] , nums[to]}

                returns  = append(returns,temp)

                for from < to && nums[from] == nums[from +1]{
                    from++
                }
                for from < to && nums[to] == nums[to -1]{
                    to --
                }

                from  ++ 
                to --
            }
        }
    } 
    return returns
}




```
