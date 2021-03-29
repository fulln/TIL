## 直线上最多的点数

给定一个二维平面，平面上有 n 个点，求最多有多少个点在同一条直线上。

示例 1:

输入: [[1,1],[2,2],[3,3]]
输出: 3
解释:
^
|
|        o
|     o
|  o  
+------------->
0  1  2  3  4
示例 2:

输入: [[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]
输出: 4
解释:
^
|
|  o
|     o        o
|        o
|  o        o
+------------------->
0  1  2  3  4  5  6

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/x2n2g1/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go

type K struct {
    m int64 //分子
    n int64 //分母
}
func maxPoints(points [][]int) int {
    n := len(points)
    if n<3 {return n}
    
    res := 0
    same := K{0,0}
    
    for i:=0;i<n-1;i++ {
        hmap := map[K]int{}
        temp := 0
        for j:=i+1;j<n;j++ {
            k := getK(points[i],points[j])
            hmap[k]++
            if k!=same {
                temp = max(temp,hmap[k])
            }
        }
        //此时，从i点出发，处于同一直线上的点最多有temp+1个
        //再加上与i点相同的点的个数hmap[same]即可
        //更新全局答案res
        res = max(res,temp+1+hmap[same])
    }
    return res
}


//根据两点求斜率
func getK(p1, p2 []int) K {
    dx := int64(p1[0]-p2[0])
    dy := int64(p1[1]-p2[1])
    if dx==0&&dy==0 {return K{int64(0),int64(0)}} //p1,p2是同一点
    if dx==0 {return K{int64(1),int64(0)}} //p1,p2斜率为无穷
    if dy==0 {return K{int64(0),int64(1)}} //p1,p2斜率为0
    if dx<0 { //统一设置dx为正
        dx=-dx
        dy=-dy
    }
    d := gcd(dx,dy)
    return K{dx/d,dy/d} //返回最简约之比
}

//最大公约数
func gcd(a, b int64) int64 {
    if a==0 {return b}
    return gcd(b%a,a)
}

func max(a, b int) int {
    if a>b {return a}
    return b
}

```
