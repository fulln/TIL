## 寻找右区间
给你一个区间数组 intervals ，其中 intervals[i] = [starti, endi] ，且每个 starti 都 不同 。

区间 i 的 右侧区间 可以记作区间 j ，并满足 startj >= endi ，且 startj 最小化 。

返回一个由每个区间 i 的 右侧区间 的最小起始位置组成的数组。如果某个区间 i 不存在对应的 右侧区间 ，则下标 i 处的值设为 -1 。

 
示例 1：

输入：intervals = [[1,2]]
输出：[-1]
解释：集合中只有一个区间，所以输出-1。
示例 2：

输入：intervals = [[3,4],[2,3],[1,2]]
输出：[-1,0,1]
解释：对于 [3,4] ，没有满足条件的“右侧”区间。
对于 [2,3] ，区间[3,4]具有最小的“右”起点;
对于 [1,2] ，区间[2,3]具有最小的“右”起点。
示例 3：

输入：intervals = [[1,4],[2,3],[3,4]]
输出：[-1,2,-1]
解释：对于区间 [1,4] 和 [3,4] ，没有满足条件的“右侧”区间。
对于 [2,3] ，区间 [3,4] 有最小的“右”起点。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/find-right-interval
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
type cp struct{
    index,val int
}

func findRightInterval(intervals [][]int) []int {
    n := len(intervals)

    left :=[]cp{}
    right :=[]cp{}
    for i := range intervals{
        left = append(left,cp{i,intervals[i][0]})
        right = append(right,cp{i,intervals[i][1]})
    }

    sort.Slice(left, func(i,j int)bool{
            return left[i].val < left[j].val
    })

    sort.Slice(right, func(i,j int)bool{
            return right[i].val < right[j].val
    })

    ans := make([]int, n)

    j := 0

    for _, p := range right {
        for j < n && left[j].val < p.val {
            j++
        }
        if j < n {
            ans[p.index] = left[j].index
        } else {
            ans[p.index] = -1
        }
    }

    return ans
}

```
