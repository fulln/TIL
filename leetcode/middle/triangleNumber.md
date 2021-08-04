## 有效三角形的个数

给定一个包含非负整数的数组，你的任务是统计其中可以组成三角形三条边的三元组个数。

示例 1:

输入: [2,2,3,4]
输出: 3
解释:
有效的组合是: 
2,3,4 (使用第一个 2)
2,3,4 (使用第二个 2)
2,2,3


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-triangle-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func triangleNumber(nums []int) int {
    l := len(nums) 
    sort.Ints(nums)
    ret := 0
    for i:= 0; i < l;i++{
        for j := i+1;j< l;j++{
            for z := j+1; z < l;z++{
                if nums[i] + nums[j] > nums[z]{
                    ret ++
                }else{
                    break
                }
            }
        }
    }
    return ret
}
```
