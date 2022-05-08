## 检查是否有合法括号字符串路径
一个括号字符串是一个 非空 且只包含 '(' 和 ')' 的字符串。如果下面 任意 条件为 真 ，那么这个括号字符串就是 合法的 。

字符串是 () 。
字符串可以表示为 AB（A 连接 B），A 和 B 都是合法括号序列。
字符串可以表示为 (A) ，其中 A 是合法括号序列。
给你一个 m x n 的括号网格图矩阵 grid 。网格图中一个 合法括号路径 是满足以下所有条件的一条路径：

路径开始于左上角格子 (0, 0) 。
路径结束于右下角格子 (m - 1, n - 1) 。
路径每次只会向 下 或者向 右 移动。
路径经过的格子组成的括号字符串是 合法 的。
如果网格图中存在一条 合法括号路径 ，请返回 true ，否则返回 false 。

 

示例 1：



输入：grid = [["(","(","("],[")","(",")"],["(","(",")"],["(","(",")"]]
输出：true
解释：上图展示了两条路径，它们都是合法括号字符串路径。
第一条路径得到的合法字符串是 "()(())" 。
第二条路径得到的合法字符串是 "((()))" 。
注意可能有其他的合法括号字符串路径。
示例 2：



输入：grid = [[")",")"],["(","("]]
输出：false
解释：两条可行路径分别得到 "))(" 和 ")((" 。由于它们都不是合法括号字符串，我们返回 false 。
```go
func hasValidPath(grid [][]byte) bool {
    
    m := len(grid)
    n := len(grid[0])
    
//     dp := make([][][]bool,100)
//     for i:= 0;i < 100;i++{
//         dp[i] = make([][]int,100)
//         for j:= 0;j < 100;j++{
//             dp[i][j] = make([]bool,200)
//         }
//     }
    
//     dp[0][0][0] = true
    
//     for i:=0;i < m;i++{
//         for j := 0;j < n,j++{
            
            
            
//         }
//     }
    
    
    // dfs超时，用dp可以
    
    var dfs func(x,y,i int)bool
    
    
    dfs = func(x,y,i int) bool{
        if x== m-1 && y == n-1{
            if grid[x][y] == ')'{
                i -- 
                if i == 0{
                    return true
                }
            }
            return false
        }
        
        
        if grid[x][y] == ')'{             
            if (i -1 < 0){
                return false
            }else{
                i-- 
            }
        }else{
            if i +1 > (m+n-1){
                return false
            }else{
                i++   
            }
        }
        
        if x + 1 >= m {
            return dfs(x,y+1,i)
        }
        
                        
        if y+1 >= n{
            return dfs(x+1,y,i) 
        }
        
        return dfs(x+1,y,i) || dfs(x,y+1,i)
    }
    
    return dfs(0,0,0)
}
```
