##  切割后面积最大的蛋糕
矩形蛋糕的高度为 h 且宽度为 w，给你两个整数数组 horizontalCuts 和 verticalCuts，其中：

 horizontalCuts[i] 是从矩形蛋糕顶部到第  i 个水平切口的距离
verticalCuts[j] 是从矩形蛋糕的左侧到第 j 个竖直切口的距离
请你按数组 horizontalCuts 和 verticalCuts 中提供的水平和竖直位置切割后，请你找出 面积最大 的那份蛋糕，并返回其 面积 。由于答案可能是一个很大的数字，因此需要将结果 对 109 + 7 取余 后返回。

 

示例 1：



输入：h = 5, w = 4, horizontalCuts = [1,2,4], verticalCuts = [1,3]
输出：4 
解释：上图所示的矩阵蛋糕中，红色线表示水平和竖直方向上的切口。切割蛋糕后，绿色的那份蛋糕面积最大。
示例 2：



输入：h = 5, w = 4, horizontalCuts = [3,1], verticalCuts = [1]
输出：6
解释：上图所示的矩阵蛋糕中，红色线表示水平和竖直方向上的切口。切割蛋糕后，绿色和黄色的两份蛋糕面积最大。
示例 3：

输入：h = 5, w = 4, horizontalCuts = [3], verticalCuts = [3]
输出：9

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-area-of-a-piece-of-cake-after-horizontal-and-vertical-cuts
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func maxArea(h int, w int, horizontalCuts []int, verticalCuts []int) int {
    const e = 1000000007
    xmax,ymax:=0,0
    sort.Ints(horizontalCuts)
    sort.Ints(verticalCuts)
    last := 0
    for _,val := range horizontalCuts{
        ymax = max(ymax,val-last)
        last = val
    }    
    ymax = max(ymax,h-last)
    last = 0
    for _,val := range verticalCuts{
        xmax = max(xmax,val-last)
        last = val
    }
    xmax = max(xmax,w-last)

    return xmax * ymax % e
}

func max(a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}
```
