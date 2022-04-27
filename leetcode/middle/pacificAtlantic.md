## 太平洋大西洋水流问题
有一个 m × n 的矩形岛屿，与 太平洋 和 大西洋 相邻。 “太平洋” 处于大陆的左边界和上边界，而 “大西洋” 处于大陆的右边界和下边界。

这个岛被分割成一个由若干方形单元格组成的网格。给定一个 m x n 的整数矩阵 heights ， heights[r][c] 表示坐标 (r, c) 上单元格 高于海平面的高度 。

岛上雨水较多，如果相邻单元格的高度 小于或等于 当前单元格的高度，雨水可以直接向北、南、东、西流向相邻单元格。水可以从海洋附近的任何单元格流入海洋。

返回网格坐标 result 的 2D 列表 ，其中 result[i] = [ri, ci] 表示雨水从单元格 (ri, ci) 流动 既可流向太平洋也可流向大西洋 。

 

示例 1：



输入: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
输出: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
示例 2：

输入: heights = [[2,1],[1,2]]
输出: [[0,0],[0,1],[1,0],[1,1]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/pacific-atlantic-water-flow
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
var dirs = []struct{ x, y int }{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}

func pacificAtlantic(heights [][]int) [][]int {
    
    m := len(heights)
    n  := len(heights[0])

    p :=make([][]bool,m)
    q :=make([][]bool,m)
    for i := range p {
        p[i] = make([]bool, n)
        q[i] = make([]bool, n)
    }


    var dfs  func(x,y int,o [][]bool)

    dfs = func(x, y int,o [][]bool){
        if o[x][y]{
            return
        }

        o[x][y] = true
        for _,d := range dirs{
            if nx,ny := x+d.x,y+d.y; 0 <= nx && nx < m && 0 <= ny && ny < n && heights[x][y] <= heights[nx][ny] {
                dfs(nx,ny,o)
            }
        } 
    }

    for i:= 0;i< m;i++{
        dfs(i,0,p)
    }

    for j:= 0;j< n;j++{
        dfs(0,j,p)
    }


    for i:= 0;i< m;i++{
        dfs(i,n-1,q)
    }

    for j:= 0;j< n;j++{
        dfs(m-1,j,q)
    }


    ret := [][]int{}

    for i, row := range p {
        for j, ok := range row {
            if ok && q[i][j] {
                ret = append(ret, []int{i, j})
            }
        }
    }

    return ret
}   
```
