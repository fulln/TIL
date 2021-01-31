## 合并区间

给出一个区间的集合，请合并所有重叠的区间。

 

示例 1:

输入: intervals = [[1,3],[2,6],[8,10],[15,18]]
输出: [[1,6],[8,10],[15,18]]
解释: 区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
示例 2:

输入: intervals = [[1,4],[4,5]]
输出: [[1,5]]
解释: 区间 [1,4] 和 [4,5] 可被视为重叠区间。
注意：输入类型已于2019年4月15日更改。 请重置默认代码定义以获取新方法签名。

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xv11yj/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func merge(intervals [][]int) [][]int {
    maps := make([]bool,100000)

    if len(intervals) == 0{
        return nil
    }
    max := -1
    min := 100000
    for i:= 0 ;i < len(intervals);i++{
        for j := intervals[i][0] ; j<= intervals[i][1]; j++{
            maps[j] = true
            if max < intervals[i][1]{
                max = intervals[i][1]
            }

            if min > intervals[i][0]{
                min = intervals[i][0]
            }
        }
    }
    returns := [][]int{}
    thisreturn:=make([]int,2)
    begin :=true
    end := true
    for i := min;i <max;i++{
        if maps[i]  && begin{
            thisreturn[0]=i
            begin = false
            end = true
        }

        if ! maps[i] && end{
            thisreturn[1] = i-1 
            returns = append(returns,thisreturn[::])
            end = false
            begin = true
        }
    } 
    thisreturn[1] = max
    returns = append(returns,thisreturn)

    return returns

}
```
