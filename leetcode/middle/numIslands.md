## 岛屿数量


给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。

岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。

此外，你可以假设该网格的四条边均被水包围。

 

示例 1：

输入：grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
输出：1
示例 2：

输入：grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
输出：3
 

提示：

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] 的值为 '0' 或 '1'

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/number-of-islands
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func numIslands(grid [][]byte) int {

    // 将所有的1变0 

    m,n := len(grid),len(grid[0])

    var dfs func(x,y int)

    ret := 0

    dfs = func(x,y int){

        if 0 > x || x >= m{

            return 

        }

        if 0 > y || y >= n{

            return 

        }

  

        if grid[x][y] == '0'{

            return 

        }

  

        grid[x][y] = '0'

  

        dfs(x+1,y) 

        dfs(x-1,y) 

        dfs(x,y+1) 

        dfs(x,y-1)  

    }    

  

    for i:=0;i<m;i++{

        for j:=0;j<n;j++{

            if grid[i][j] == '1'{

                dfs(i,j)

                ret++

            }

        }

    }

  

    return ret

}
```