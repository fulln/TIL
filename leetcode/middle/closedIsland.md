##  统计封闭岛屿的数目
有一个二维矩阵 grid ，每个位置要么是陆地（记号为 0 ）要么是水域（记号为 1 ）。

我们从一块陆地出发，每次可以往上下左右 4 个方向相邻区域走，能走到的所有陆地区域，我们将其称为一座「岛屿」。

如果一座岛屿 完全 由水域包围，即陆地边缘上下左右所有相邻区域都是水域，那么我们将其称为 「封闭岛屿」。

请返回封闭岛屿的数目。

 

示例 1：



输入：grid = [[1,1,1,1,1,1,1,0],[1,0,0,0,0,1,1,0],[1,0,1,0,1,1,1,0],[1,0,0,0,0,1,0,1],[1,1,1,1,1,1,1,0]]
输出：2
解释：
灰色区域的岛屿是封闭岛屿，因为这座岛屿完全被水域包围（即被 1 区域包围）。
示例 2：



输入：grid = [[0,0,1,0,0],[0,1,0,1,0],[0,1,1,1,0]]
输出：1
示例 3：

输入：grid = [[1,1,1,1,1,1,1],
             [1,0,0,0,0,0,1],
             [1,0,1,1,1,0,1],
             [1,0,1,0,1,0,1],
             [1,0,1,1,1,0,1],
             [1,0,0,0,0,0,1],
             [1,1,1,1,1,1,1]]
输出：2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-closed-islands
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func closedIsland(grid [][]int) int {

    count :=0
    for i:=0;i< len(grid);i++{
        for j:=0;j< len(grid[0]);j++{
            if grid[i][j] == 0 && errorland(i,j,grid){
                count ++   
            }
        }
    }

    return count
}

func errorland(i,j int,grid [][]int)bool{
    if i < 0 || i >= len(grid) || j <0 || j >= len(grid[0]){
        return false
    } 

    if grid[i][j] == 0{
        grid[i][j] = 1
        left := errorland(i,j-1,grid)
        right := errorland(i,j+1,grid)
        up := errorland(i+1,j,grid)
        down := errorland(i-1,j,grid)
        return left && right && up && down
    }

    return true;
}
```
