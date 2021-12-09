## 有效的井字游戏

你一个字符串数组 board 表示井字游戏的棋盘。当且仅当在井字游戏过程中，棋盘有可能达到 board 所显示的状态时，才返回 true 。

井字游戏的棋盘是一个 3 x 3 数组，由字符 ' '，'X' 和 'O' 组成。字符 ' ' 代表一个空位。

以下是井字游戏的规则：

玩家轮流将字符放入空位（' '）中。
玩家 1 总是放字符 'X' ，而玩家 2 总是放字符 'O' 。
'X' 和 'O' 只允许放置在空位中，不允许对已放有字符的位置进行填充。
当有 3 个相同（且非空）的字符填充任何行、列或对角线时，游戏结束。
当所有位置非空时，也算为游戏结束。
如果游戏结束，玩家不允许再放置字符。


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-tic-tac-toe-state
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func validTicTacToe(board []string) bool {
    yes := "O"
    no := "X"
    //1. 是否停止
    //2. 停止时对面是否没达成条件
    // 这里直接模拟
    onum :=0
    xnum := 0
    for i := 0 ;i < 9;i++{
        x := i / 3
        y := i % 3        
        if string(board[x][y]) == yes{
            onum ++
        }
        if string(board[x][y]) == no{
            xnum ++
        }
    }
    y := effects(board,yes)
    n := effects(board,no)

    return !(onum != xnum && onum != xnum-1 ||
        onum != xnum && y ||
        onum != xnum-1 && n)
}

func effects(board []string, p string)bool{
    for i:=0;i< 3;i++{
        if string(board[i][0]) == p && string(board[i][1]) == p  && string(board[i][2]) == p ||
            string(board[0][i]) == p && string(board[1][i]) == p  && string(board[2][i]) == p{
                return true 
            }            
    }
    return string(board[0][0]) ==p && string(board[1][1]) ==p  && string(board[2][2]) == p ||
         string(board[0][2]) == p &&  string(board[1][1]) ==p &&  string(board[2][0]) == p
}
```
