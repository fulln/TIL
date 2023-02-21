## 79. 单词搜索
给定一个 m x n 二维字符网格 board 和一个字符串单词 word 。如果 word 存在于网格中，返回 true ；否则，返回 false 。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

 

示例 1：


输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
输出：true
示例 2：


输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
输出：true
示例 3：


输入：board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
输出：false
 

提示：

m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board 和 word 仅由大小写英文字母组成

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/word-search
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```java
func exist(board [][]byte, word string) bool {

    // 剪枝

    m,n := len(board),len(board[0])

  

    exists := make([][]bool,m)

    for i := 0;i < m;i++{

        exists[i] = make([]bool,n)

    }

  

    var dfs func(x,y,tm int)bool

    rans := [][]int{[]int{0,1},[]int{0,-1},[]int{1,0},[]int{-1,0}}

    dfs = func(x,y,tm int)bool{

        if x < 0|| x >= m{

            return false

        }

        if y < 0|| y >= n{

            return false

        }

        if exists[x][y] {

            return false

        } 

        if board[x][y] != word[tm] {

            return false

        }

        if tm == len(word)-1{

            return true

        }

        exists[x][y] = true

        for i:=0;i< 4;i++{

            tempx :=x + rans[i][0]

            tempy :=y + rans[i][1] 

           if dfs(tempx,tempy,tm+1) {

               return true

           }

        }

        exists[x][y] = false

        return false

    }

  

    ret := false

    for i:=0;i<m;i++{

        for j :=0;j < n;j++{

            ret = dfs(i,j,0)

            if ret {

                return ret

            }

        }

    } 

    return ret

}
```