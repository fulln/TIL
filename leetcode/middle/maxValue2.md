## 剑指 Offer 47. 礼物的最大价值

剑指 Offer 47. 礼物的最大价值
在一个 mn 的棋盘的每一格都放有一个礼物，每个礼物都有一定的价值（价值大于 0）。你可以从棋盘的左上角开始拿格子里的礼物，并每次向右或者向下移动一格、直到到达棋盘的右下角。给定一个棋盘及其上面的礼物的价值，请计算你最多能拿到多少价值的礼物？

 

示例 1:

输入: 
[
  [1,3,1],
  [1,5,1],
  [4,2,1]

]
输出: 12
解释: 路径 1→3→5→2→1 可以拿到最多价值的礼物


```go

func maxValue(grid [][]int) int {
    x := len(grid)
    y := len(grid[0])
    dp :=make([][]int,x)
    
    for m:=0;m<len(dp);m++{
        dp[m] = make([]int,y+1)
    }

    dp[0][0] = grid[0][0]
    
    for i :=1;i< x;i++{
        dp[i][0] = dp[i-1][0]+grid[i][0]
    }

    for j :=1;j< y;j++{
        dp[0][j] = dp[0][j-1]+grid[0][j]
    }


    for i:=1;i< x;i++{
        for j:=1;j< y;j++{
            dp[i][j] = Max(dp[i-1][j],dp[i][j-1]) + grid[i][j]
        } 
    }

    return dp[x-1][y-1]
}


func Max (a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}


```
