## 骑士在棋盘上的概率
在一个 n x n 的国际象棋棋盘上，一个骑士从单元格 (row, column) 开始，并尝试进行 k 次移动。行和列是 从 0 开始 的，所以左上单元格是 (0,0) ，右下单元格是 (n - 1, n - 1) 。

象棋骑士有8种可能的走法，如下图所示。每次移动在基本方向上是两个单元格，然后在正交方向上是一个单元格。



每次骑士要移动时，它都会随机从8种可能的移动中选择一种(即使棋子会离开棋盘)，然后移动到那里。

骑士继续移动，直到它走了 k 步或离开了棋盘。

返回 骑士在棋盘停止移动后仍留在棋盘上的概率 。



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/knight-probability-in-chessboard
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处
```go
func knightProbability(n int, k int, row int, column int) float64 {
    dp := make([][][]float64, n)
    for i := 0; i < n; i++ {
        dp[i] = make([][]float64, n)
        for j := 0; j < n; j++ {
            dp[i][j] = make([]float64, k + 1)
            dp[i][j][0] = 1
        }
    }
    for i := 1; i <= k; i++ {
        for r := 0; r < n; r++ {
            for c := 0; c < n; c++ {
                for _, dir := range [][]int{{1, 2}, {2, 1}, {-2, 1}, {1, -2}, {2, -1}, {-1, 2}, {-1, -2}, {-2, -1}} {
                    nr, nc := r + dir[0], c + dir[1]
                    if nr >= 0 && nr < n && nc >= 0 && nc < n {
                        dp[r][c][i] += dp[nr][nc][i-1]/8
                    }
                }
            }
        }
    }
    return dp[row][column][k]
}

```
