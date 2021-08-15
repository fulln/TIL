## 出界的路径数
给你一个大小为 m x n 的网格和一个球。球的起始坐标为 [startRow, startColumn] 。你可以将球移到在四个方向上相邻的单元格内（可以穿过网格边界到达网格之外）。你 最多 可以移动 maxMove 次球。

给你五个整数 m、n、maxMove、startRow 以及 startColumn ，找出并返回可以将球移出边界的路径数量。因为答案可能非常大，返回对 109 + 7 取余 后的结果。

 

示例 1：


输入：m = 2, n = 2, maxMove = 2, startRow = 0, startColumn = 0
输出：6
示例 2：


输入：m = 1, n = 3, maxMove = 3, startRow = 0, startColumn = 1
输出：12

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/out-of-boundary-paths
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
//dfs
func findPaths(m int, n int, maxMove int, startRow int, startColumn int) int {
    ret := 0
    
    var dfs func(x,y,curr int)
    dfs = func(x,y,curr int){
        if x >= m || x < 0 || y >= n || y < 0{
            ret++
            return 
        }
        if curr >= maxMove{
            return 
        }
        curr += 1
        dfs(x+1,y,curr)
        dfs(x,y+1,curr)
        dfs(x-1,y,curr)
        dfs(x,y-1,curr)
        curr -= 1
    }
    dfs(startRow,startColumn,0) 
    return ret 
}
//dp
func findPaths(m int, n int, maxMove int, startRow int, startColumn int) int {
    ret := 0
    dp := make([][][]int, maxMove+1)
    for i := range dp {
        dp[i] = make([][]int, m+2) 
        for j := range dp[i] {
            dp[i][j] = make([]int, n+2)
        }
    }
    
    dp[0][startRow+1][startColumn+1] = 1
    for k:=1; k <= maxMove; k++ { 
        for i:=0; i <= m+1 ; i++ {
            for j:=0; j <= n+1; j++ { 
                if !ok(m,n,i,j) {
                    dp[k][i][j] = dp[k-1][i][j]
                }              
                if ok(m,n,i-1,j) {
                    dp[k][i][j] += dp[k-1][i-1][j]
                }
                if ok(m,n,i+1,j) {
                    dp[k][i][j] += dp[k-1][i+1][j]
                }
                if ok(m,n,i,j-1) {
                    dp[k][i][j] += dp[k-1][i][j-1]
                }
                if ok(m,n,i,j+1) {
                    dp[k][i][j] += dp[k-1][i][j+1]
                }
                dp[k][i][j] %= 1000000007
                // sum 
                if k == maxMove && !ok(m,n,i,j) {                
                    ret += dp[k][i][j]     
                    ret = ret % 1000000007  
                }
            }
        }
       
    } 
   
    return ret
} 

func ok(m,n, i,j int) bool { // 在方格內
    if i>=1 && i <= m && j >=1 && j <= n {
        return true
    }
    return false
}

```

