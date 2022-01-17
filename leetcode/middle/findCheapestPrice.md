## K 站中转内最便宜的航班
有 n 个城市通过一些航班连接。给你一个数组 flights ，其中 flights[i] = [fromi, toi, pricei] ，表示该航班都从城市 fromi 开始，以价格 pricei 抵达 toi。

现在给定所有的城市和航班，以及出发城市 src 和目的地 dst，你的任务是找到出一条最多经过 k 站中转的路线，使得从 src 到 dst 的 价格最便宜 ，并返回该价格。 如果不存在这样的路线，则输出 -1。

 

示例 1：

输入: 
n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 1
输出: 200
解释: 
城市航班图如下


从城市 0 到城市 2 在 1 站中转以内的最便宜价格是 200，如图中红色所示。
示例 2：

输入: 
n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 0
输出: 500
解释: 
城市航班图如下


从城市 0 到城市 2 在 0 站中转以内的最便宜价格是 500，如图中蓝色所示。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/cheapest-flights-within-k-stops
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
##  K 站中转内最便宜的航班

有 n 个城市通过一些航班连接。给你一个数组 flights ，其中 flights[i] = [fromi, toi, pricei] ，表示该航班都从城市 fromi 开始，以价格 pricei 抵达 toi。

现在给定所有的城市和航班，以及出发城市 src 和目的地 dst，你的任务是找到出一条最多经过 k 站中转的路线，使得从 src 到 dst 的 价格最便宜 ，并返回该价格。 如果不存在这样的路线，则输出 -1。

 

示例 1：

输入: 
n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 1
输出: 200
解释: 
城市航班图如下


从城市 0 到城市 2 在 1 站中转以内的最便宜价格是 200，如图中红色所示。
示例 2：

输入: 
n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
src = 0, dst = 2, k = 0
输出: 500
解释: 
城市航班图如下


从城市 0 到城市 2 在 0 站中转以内的最便宜价格是 500，如图中蓝色所示。
 

提示：

1 <= n <= 100
0 <= flights.length <= (n * (n - 1) / 2)
flights[i].length == 3
0 <= fromi, toi < n
fromi != toi
1 <= pricei <= 104
航班没有重复，且不存在自环
0 <= src, dst, k < n
src != dst

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/cheapest-flights-within-k-stops
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func findCheapestPrice(n int, flights [][]int, src int, dst int, k int) int {
    // 每条路径去尝试,然后记录价格,
    // 到达终点最便宜路线为 到达终点前最便宜路线点+ 该点到终点的路线
    // 有数组滚动
    // 是动态规化 航班没有重复，且不存在自环  
    // 需要知道,每个节点对应的能去的下一个节点,但是这个时间复杂度是o(n^2) 空间复杂度也是o(n^2)感觉计算了很多没必要的计算 


    // 方法2   典型prim  最小生成树(不知道)
    dp := make([][]int,n)
    inf := 1000* 101+1
    for i :=range dp{
        dp[i]  =  make([]int,k+2)
        for j := range dp[i]{
                dp[i][j] = inf
        }
    }
   
    dp[src][0] = 0;

    for i:=1;i< k+2;i++{
        for _,val := range flights{
                dp[val[1]][i] = min(dp[val[1]][i],dp[val[0]][i-1] + val[2])
        }
    }

    res := inf
    for i:=1;i<k+2;i++{
        res = min(res,dp[dst][i])
    }

    if res == inf {
        return -1
    }else{
        return res
    }
}

func min(a,b int)int{
    if a < b{
        return a
    }else{
        return b
    }
}
```
```
