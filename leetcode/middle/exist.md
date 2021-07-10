## 单词搜索
给定一个二维网格和一个单词，找出该单词是否存在于网格中。

单词必须按照字母顺序，通过相邻的单元格内的字母构成，其中“相邻”单元格是那些水平相邻或垂直相邻的单元格。同一个单元格内的字母不允许被重复使用。

 

示例:

board =
[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]

给定 word = "ABCCED", 返回 true
给定 word = "SEE", 返回 true
给定 word = "ABCB", 返回 false
 

提示：

board 和 word 中只包含大写和小写英文字母。
1 <= board.length <= 200
1 <= board[i].length <= 200
1 <= word.length <= 10^3

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvkwe2/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go

func exist(board [][]byte, word string) bool {

	bools := make([][]bool,len(board))

	for i:=0;i< len(bools);i++{
		bools[i] =make([]bool,len(board[0]))
	}


	var dfs func(i,j ,index int)bool

	dfs  = func(i,j,index int)bool{
		if index == len(word){
			return true
		}
		if i < 0  || i >= len(board) {
			return false
		}
		if j < 0  || j >= len(board[0]) {
			return false
		}

		if board[i][j] == word[index]  && bools[i][j] == false{

			bools[i][j] = true

			ret1 := dfs(i,j+1,index + 1)
			ret2 := dfs(i,j-1,index + 1)
			ret3 := dfs(i-1,j,index + 1)
			ret4 := dfs(i+1,j,index + 1)

			if ret1 || ret2 || ret3 || ret4 {
				return true
			}else{
				bools[i][j] = false
				return false
			}
		}else{
			return false
		}
	}
    
    for i:=0;i< len(board);i++{
		for j :=0;j<len(board[0]);j++{
			if dfs(i,j,0)  == true{
				return true
			}
		}
	}

	return false


}


```
