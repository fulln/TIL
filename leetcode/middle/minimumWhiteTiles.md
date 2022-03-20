## 6023. 用地毯覆盖后的最少白色砖块

给你一个下标从 0 开始的 二进制 字符串 floor ，它表示地板上砖块的颜色。

floor[i] = '0' 表示地板上第 i 块砖块的颜色是 黑色 。
floor[i] = '1' 表示地板上第 i 块砖块的颜色是 白色 。
同时给你 numCarpets 和 carpetLen 。你有 numCarpets 条 黑色 的地毯，每一条 黑色 的地毯长度都为 carpetLen 块砖块。请你使用这些地毯去覆盖砖块，使得未被覆盖的剩余 白色 砖块的数目 最小 。地毯相互之间可以覆盖。

请你返回没被覆盖的白色砖块的 最少 数目。

 

示例 1：



输入：floor = "10110101", numCarpets = 2, carpetLen = 2
输出：2
解释：
上图展示了剩余 2 块白色砖块的方案。
没有其他方案可以使未被覆盖的白色砖块少于 2 块。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-white-tiles-after-covering-with-carpets
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func minimumWhiteTiles(floor string, numCarpets int, carpetLen int) int {
        dp := make([][]int,numCarpets+1)
        for i:=0;i< len(dp);i++{
            dp[i] =  make([]int,len(floor))
            if i == 0{
                dp[0][0]  = int(floor[0]- '0')
                for j:= 1;j< len(floor);j++{
                    dp[0][j]= dp[0][j-1] + int(floor[j]- '0') 
                }
            }           
        }

       	for a := 1; a <= numCarpets; a++ {
            for b := carpetLen * a; b < len(floor); b++ {
                dp[a][b] = min(dp[a][b-1]+int(floor[b]- '0'), dp[a-1][b-carpetLen])
            }
	    }

        return dp[numCarpets][len(floor)-1]
}



func min(a,b int)int{
    if a > b{
        return b
    }else{
        return a
    }
}
```
