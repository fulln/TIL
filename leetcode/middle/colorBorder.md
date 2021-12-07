## 边界着色
给你一个大小为 m x n 的整数矩阵 grid ，表示一个网格。另给你三个整数 row、col 和 color 。网格中的每个值表示该位置处的网格块的颜色。

两个网格块属于同一 连通分量 需满足下述全部条件：

两个网格块颜色相同
在上、下、左、右任意一个方向上相邻
连通分量的边界 是指连通分量中满足下述条件之一的所有网格块：

在上、下、左、右四个方向上与不属于同一连通分量的网格块相邻
在网格的边界上（第一行/列或最后一行/列）
请你使用指定颜色 color 为所有包含网格块 grid[row][col] 的 连通分量的边界 进行着色，并返回最终的网格 grid 。

 

示例 1：

输入：grid = [[1,1],[1,2]], row = 0, col = 0, color = 3
输出：[[3,3],[3,2]]
示例 2：

输入：grid = [[1,2,2],[2,3,2]], row = 0, col = 1, color = 3
输出：[[1,3,3],[2,3,3]]
示例 3：

输入：grid = [[1,1,1],[1,1,1],[1,1,1]], row = 1, col = 1, color = 2
输出：[[2,2,2],[2,1,2],[2,2,2]]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/coloring-a-border
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func dfs(grid [][]int, row , col, color ,pre int,mask [][]int)  { //pre为初始格子的颜色
	//判断返回当条件，当不在矩阵中或者颜色不是pre,就可以返回了
	if row<0 || row>=len(grid) || col<0 || col>=len(grid[0]) || grid[row][col] != pre{
		return
	}
	grid[row][col] = color   //把联通分量都着色
	mask[row][col] = 1        //mask数组记录哪些是联通分量

	di := []int{1,-1,0,0}     //创建这样的两个数组，方便后边往四个方向深度搜索
	dj := []int{0,0,1,-1}     //会很常用的，往多个方向搜索
	for i := 0; i < 4; i++ {  //四个方向进行深度搜索
		dfs(grid,row+di[i],col+dj[i],color,pre,mask)
	}
}

func colorBorder(grid [][]int, row int, col int, color int) [][]int {
	if grid[row][col] == color {   //初始给定的格子颜色和给的color一样 直接返回grid
		return grid  
	}
	pre := grid[row][col]           //记初始格子颜色为pre

	//下面为go语言创建二维切片的方法
	mask := make([][]int,len(grid))   //创建mask 用make开辟外层的长度
	for i:=range mask{                 //遍历以开辟里面一层的长度
		mask[i] = make([]int ,len(grid[0]))
	}


	dfs(grid,row,col,color,pre,mask)   //开始dfs
	for i := 1; i < len(grid)-1; i++ { //遍历矩阵的中间部分  将联通分量的中间部分该为原来的颜色pre
		for j := 1; j < len(grid[0])-1; j++ {
			if mask[i][j] == 1 && mask[i-1][j] == 1 &&mask[i+1][j]==1&&mask[i][j-1]==1&&mask[i][j+1]==1{
				grid[i][j] = pre
			}
		}
	}
	return grid
}

```
