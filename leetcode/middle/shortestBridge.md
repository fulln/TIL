## 934. 最短的桥
给你一个大小为 n x n 的二元矩阵 grid ，其中 1 表示陆地，0 表示水域。

岛 是由四面相连的 1 形成的一个最大组，即不会与非组内的任何其他 1 相连。grid 中 恰好存在两座岛 。

你可以将任意数量的 0 变为 1 ，以使两座岛连接起来，变成 一座岛 。

返回必须翻转的 0 的最小数目。

 

示例 1：

输入：grid = [[0,1],[1,0]]
输出：1
示例 2：

输入：grid = [[0,1,0],[0,0,0],[0,0,1]]
输出：2
示例 3：

输入：grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
输出：1
 

提示：

n == grid.length == grid[i].length
2 <= n <= 100
grid[i][j] 为 0 或 1
grid 中恰有两个岛

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/shortest-bridge
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func shortestBridge(grid [][]int) int {
    n := len(grid)
    ret:= 0
    exists := [][]int{}
    var  bfs func(i,j int)
    bfs = func(i,j int){
        if i < 0 || i >= n || j >=n || j < 0{
            return
        }        
        if grid[i][j] == 1 {
            exists =append(exists,[]int{i,j})
            grid[i][j] = -1
            bfs(i,j+1)
            bfs(i,j-1)
            bfs(i-1,j)
            bfs(i+1,j)
        }
    }
    
    out:
    for i:=0;i < n;i++{
        for j :=0;j < n;j++{
            if grid[i][j] == 1{
                exists =append(exists,[]int{i,j})                                
                grid[i][j] = -1
                bfs(i,j+1)
                bfs(i,j-1)
                bfs(i-1,j)
                bfs(i+1,j)                                
                break out
            }
        }
    }    
    pairs := [][]int{{0,1},{0,-1},{1,0},{-1,0}}
    check:
    for {    
        l := len(exists);
        for _,val := range exists{                        
            for _,p :=range pairs{                
                i,j := val[0]+p[0],val[1]+p[1]            
                if i < 0 ||i >=n ||j <0|| j>= n{
                    continue
                }
                if grid[i][j] == -1{
                    continue
                }
                
                if grid[i][j] == 0{
                    exists =append(exists,[]int{i,j})
                    grid[i][j] = -1
                    continue
                }

                if grid[i][j] == 1{
                    break check
                }
            }
        }
        ret++
        exists = exists[l:]
    }


    return ret
}

func min(a,b int)int{
    if a > b{
        return b
    }else{
        return a
    }
}

```
