## 98. 对角线遍历

给你一个大小为 m x n 的矩阵 mat ，请以对角线遍历的顺序，用一个数组返回这个矩阵中的所有元素。

 

示例 1：


输入：mat = [[1,2,3],[4,5,6],[7,8,9]]
输出：[1,2,4,7,5,3,6,8,9]
示例 2：

输入：mat = [[1,2],[3,4]]
输出：[1,2,3,4]
 

提示：

m == mat.length
n == mat[i].length
1 <= m, n <= 104
1 <= m * n <= 104
-105 <= mat[i][j] <= 105

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/diagonal-traverse
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func findDiagonalOrder(mat [][]int) []int {
    m,n := len(mat),len(mat[0])
    ret := []int{}    
    for j:=0 ;j< m+ n-1; j++{
        if j & 1 == 1{
            x := max(j - n + 1, 0)
            y := min(j, n-1)
            for x < m && y >= 0 {
                ret = append(ret, mat[x][y])
                x++
                y--
            }
        }else{
            x := min(j, m-1)
            y := max(j-m + 1, 0)
            for x >= 0 && y < n {
                ret = append(ret, mat[x][y])
                x--
                y++
            }
        }
    }
    return ret
}

func min(a,b int)int{
    if a < b{
        return a
    }else{
        return b
    }
}


func max(a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}
```
