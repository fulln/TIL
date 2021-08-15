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
```
