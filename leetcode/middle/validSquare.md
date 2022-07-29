## 有效的正方形
给定2D空间中四个点的坐标 p1, p2, p3 和 p4，如果这四个点构成一个正方形，则返回 true 。

点的坐标 pi 表示为 [xi, yi] 。输入 不是 按任何顺序给出的。

一个 有效的正方形 有四条等边和四个等角(90度角)。

 

示例 1:

输入: p1 = [0,0], p2 = [1,1], p3 = [1,0], p4 = [0,1]
输出: True
示例 2:

输入：p1 = [0,0], p2 = [1,1], p3 = [1,0], p4 = [0,12]
输出：false
示例 3:

输入：p1 = [1,0], p2 = [-1,0], p3 = [0,1], p4 = [0,-1]
输出：true

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/valid-square
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func validSquare(p1 []int, p2 []int, p3 []int, p4 []int) bool {
    sets := [][]int{p1,p2,p3,p4}
    maps := make(map[int]int)
    for i:=0;i<4;i++{        
        for j:= 0;  j < 4;j++{
            if j == i{
                continue
            }
            x := row(sets[i][0],sets[j][0],sets[i][1],sets[j][1])
            if x == 0 {
                return false
            }
            maps[x] += 1
        }    
    }
    if len(maps) != 2 {
        return false
    }
    return true
}

func row(a,b,x,y int)int{
    return abs(a-b)*abs(a-b) + abs(x-y)*abs(x-y)
}

func abs(a int)int{
    if a < 0{
        return -1 * a
    }else{
        return a
    }
}
```
