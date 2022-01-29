## 地图中的最高点
给你一个大小为 m x n 的整数矩阵 isWater ，它代表了一个由 陆地 和 水域 单元格组成的地图。

如果 isWater[i][j] == 0 ，格子 (i, j) 是一个 陆地 格子。
如果 isWater[i][j] == 1 ，格子 (i, j) 是一个 水域 格子。
你需要按照如下规则给每个单元格安排高度：

每个格子的高度都必须是非负的。
如果一个格子是是 水域 ，那么它的高度必须为 0 。
任意相邻的格子高度差 至多 为 1 。当两个格子在正东、南、西、北方向上相互紧挨着，就称它们为相邻的格子。（也就是说它们有一条公共边）
找到一种安排高度的方案，使得矩阵中的最高高度值 最大 。

请你返回一个大小为 m x n 的整数矩阵 height ，其中 height[i][j] 是格子 (i, j) 的高度。如果有多种解法，请返回 任意一个 。

 

示例 1：



输入：isWater = [[0,1],[0,0]]
输出：[[1,0],[2,1]]
解释：上图展示了给各个格子安排的高度。
蓝色格子是水域格，绿色格子是陆地格。
示例 2：



输入：isWater = [[0,0,1],[1,0,0],[0,0,0]]
输出：[[1,1,0],[0,1,1],[1,2,2]]
解释：所有安排方案中，最高可行高度为 2 。
任意安排方案中，只要最高高度为 2 且符合上述规则的，都为可行方案。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/map-of-highest-peak
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func highestPeak(isWater [][]int) [][]int {
	list := make([][]int, 0)

	for i := 0; i < len(isWater); i++ {
		for j := 0; j < len(isWater[0]); j++ {
			if isWater[i][j] == 1 {
				list = append(list, []int{i, j})
				isWater[i][j] = 0
			} else {
				isWater[i][j] = -1
			}
		}
	}

	next := [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
	step := 0
	for len(list) > 0 {
		size := len(list)
		step++
		for ; size > 0; size-- {

			point := list[0]

			list = list[1:]
			for i := 0; i < 4; i++ {
				nx := point[0] + next[i][0]
				ny := point[1] + next[i][1]

				if nx >= 0 && ny >= 0 && nx < len(isWater) && ny < len(isWater[0]) && isWater[nx][ny] == -1 {

					list = append(list, []int{nx, ny})
					isWater[nx][ny] = step
				}
			}

		}
	}
	return isWater
}
```
