## 回旋镖的数量

给定平面上 n 对 互不相同 的点 points ，其中 points[i] = [xi, yi] 。回旋镖 是由点 (i, j, k) 表示的元组 ，其中 i 和 j 之间的距离和 i 和 k 之间的距离相等（需要考虑元组的顺序）。

返回平面上所有回旋镖的数量。

 
示例 1：

输入：points = [[0,0],[1,0],[2,0]]
输出：2
解释：两个回旋镖为 [[1,0],[0,0],[2,0]] 和 [[1,0],[2,0],[0,0]]
示例 2：

输入：points = [[1,1],[2,2],[3,3]]
输出：2
示例 3：

输入：points = [[1,1]]
输出：0
```go

func numberOfBoomerangs(points [][]int) int {
    var nums map[int]int
    sum := 0
    for _,i:= range points{
        nums =make(map[int]int)
        for _,j := range points{
            p :=(i[0]-j[0])*(i[0]-j[0]) + (i[1]-j[1])*(i[1]-j[1])
            nums[p]++
        }
        for _,val :=range nums{
            sum+= val*(val -1)
        }
    }
    return sum

}

```