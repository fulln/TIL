## 剑指 Offer 61. 扑克牌中的顺子

从扑克牌中随机抽5张牌，判断是不是一个顺子，即这5张牌是不是连续的。2～10为数字本身，A为1，J为11，Q为12，K为13，而大、小王为 0 ，可以看成任意数字。A 不能视为 14。

 

示例 1:

输入: [1,2,3,4,5]
输出: True
 

示例 2:

输入: [0,0,1,2,5]
输出: True

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/bu-ke-pai-zhong-de-shun-zi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func isStraight(nums []int) bool {

    maps := make(map[int]int,5)
    max:= -1
    min:= 14
    zeros:= 0
    for i:= 0;i< len(nums);i++{

        if nums[i] == 0{
            zeros +=1
            continue
        }

        if maps[nums[i]] == 1{
            return false
        } else{
            maps[nums[i]] +=1
        }

       
        if min > nums[i]{
            min = nums[i]
            
        }
        if max < nums[i]{
            max = nums[i]
        }          
    }

    if zeros >= 4{
        return true
    }

    if max - min >4{        
        return false
    }
    return true
}
```
