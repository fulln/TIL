## 求众数 II
给定一个大小为 n 的整数数组，找出其中所有出现超过 ⌊ n/3 ⌋ 次的元素。

 

 

示例 1：

输入：[3,2,3]
输出：[3]
示例 2：

输入：nums = [1]
输出：[1]
示例 3：

输入：[1,1,1,3,3,2,2,2]
输出：[1,2]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/majority-element-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```gofunc majorityElement(nums []int) []int {

    l1,l2,cons1,cons2 :=0,0,0,0

    for i:=0;i< len(nums);i++{
        if l1 > 0 && cons1 ==  nums[i]{
            l1 ++
        } else if l2 > 0 && cons2 ==  nums[i]{
            l2 ++
        }else if l1 == 0{
            cons1 = nums[i]
            l1 ++
        }else if l2 == 0{
            cons2 = nums[i]
            l2 ++
        }else{
            l1--
            l2--
        }
    }

    cnt1, cnt2 := 0, 0
    for _, num := range nums {
        if l1 > 0 && num == cons1 {
            cnt1++
        }
        if l2 > 0 && num == cons2 {
            cnt2++
        }
    }

    ret := []int{}
    if l1 > 0 && cnt1 > len(nums)/3 {
        ret =append(ret,cons1)
    }
    if l2 > 0  && cnt2 > len(nums)/3{
        ret =append(ret,cons2)
    }

    return ret
}
```
