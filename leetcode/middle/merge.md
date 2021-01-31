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
   lens := len(intervals)

    if lens <= 1{
        return intervals
    }


   qsort(0,lens-1,intervals)

   returns := [][]int{}
   lastMax := -1
   for i:= 0;i < lens ;i++{

       if lastMax != -1 &&  intervals[i][0] <= lastMax{
           returns[len(returns) -1][1] = max(intervals[i][1],lastMax)
           lastMax = max(intervals[i][1],lastMax)
           continue
       }
      returns = append(returns,intervals[i])
      lastMax = max(intervals[i][1],lastMax)
       
   }

   return returns

}

func max(a,b int)int{
    if a > b{
        return a
    }

    return b
}

//手写快排
func qsort(from,to int,res [][]int){
    begin := from
    end := to
    index := from
    if from >= to{
        return
    }

    for begin < end{
        for begin < end{
            if res[index][0] <= res[end][0]{
                end -- 
                continue
            }            
            res[index] ,res[end] = res[end],res[index]
            index =  end
            break
        }

        for begin < end{
            if res[index][0] >= res[begin][0]{
                begin ++ 
                continue
            }            
            res[index] ,res[begin] = res[begin],res[index]
            index =  begin
            break
        }
    }

    qsort(from,index-1,res)
    qsort(index+1,to,res)

}
```
