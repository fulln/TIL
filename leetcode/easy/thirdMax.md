##  第三大的数

给定一个非空数组，返回此数组中第三大的数。如果不存在，则返回数组中最大的数。要求算法时间复杂度必须是O(n)。

示例 1:

输入: [3, 2, 1]

输出: 1

解释: 第三大的数是 1.
示例 2:

输入: [1, 2]

输出: 2

解释: 第三大的数不存在, 所以返回最大的数 2 .
示例 3:

输入: [2, 2, 3, 1]

输出: 1

解释: 注意，要求返回第三大的数，是指第三大且唯一出现的数。
存在两个值为2的数，它们都排第二。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/third-maximum-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func thirdMax(nums []int) int {
    ints := []int{math.MinInt64, math.MinInt64, math.MinInt64}
    
    for _,v := range nums{
            if ints[0] ==  v ||ints[1] ==  v||ints[2] ==  v{
                continue
            }

            if ints[2] < v {
                ints[0] = ints[1]
                ints[1] = ints[2]
                ints[2] = v
            }else if ints[1] < v {
                ints[0] = ints[1]
                ints[1] = v
            }else if ints[0] < v{
                ints[0] = v
            }
    }

        if ints[0] > math.MinInt64 {
            return ints[0] 
        }

        return ints[2] 

}
```
