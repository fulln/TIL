## 连接所有点的最小费用

给你一个points 数组，表示 2D 平面上的一些点，其中 points[i] = [xi, yi] 。

连接点 [xi, yi] 和点 [xj, yj] 的费用为它们之间的 曼哈顿距离 ：|xi - xj| + |yi - yj| ，其中 |val| 表示 val 的绝对值。

请你返回将所有点连接的最小总费用。只有任意两点之间 有且仅有 一条简单路径时，才认为所有点都已连接。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/min-cost-to-connect-all-points
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func minCostConnectPoints(points [][]int) int {
	ln := len(points)
	vis := make([]bool, ln)
	dict := make([]int, ln+1)

	for i:=0;i<ln+1;i++ {
		dict[i] = math.MaxInt64
	}
	dict[0] = 0
	vis[0] = true

	ans := 0
	temp := 0
	for i:=1;i<ln;i++ {
		min := ln
		for j:=0;j<ln;j++ {
			d := calcDict(points[temp][0],points[temp][1],points[j][0],points[j][1])
			if !vis[j] && d < dict[j] {
				dict[j] = d
			}
		}
		for j:=0;j<ln;j++ {
			if dict[j]<dict[min] && !vis[j] {
				min = j
			}
		}
		vis[min] = true
		ans += dict[min]
		temp = min
	}
	return ans
}

func calcDict(x1, y1 int, x2, y2 int) int {
	x := math.Abs(float64(x1-x2))
	y := math.Abs(float64(y1-y2))
	return int(x+y)
}

作者：qianshui-2c
链接：https://leetcode-cn.com/problems/min-cost-to-connect-all-points/solution/biao-zhun-primsuan-fa-by-qianshui-2c-f8xz/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```
