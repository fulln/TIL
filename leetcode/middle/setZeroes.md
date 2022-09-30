## 面试题 01.08. 零矩阵
编写一种算法，若M × N矩阵中某个元素为0，则将其所在的行与列清零。

 

示例 1：

输入：
[
  [1,1,1],
  [1,0,1],
  [1,1,1]
]
输出：
[
  [1,0,1],
  [0,0,0],
  [1,0,1]
]
示例 2：

输入：
[
  [0,1,2,0],
  [3,4,5,2],
  [1,3,1,5]
]
输出：
[
  [0,0,0,0],
  [0,4,5,0],
  [0,3,1,0]
]

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/zero-matrix-lcci
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func setZeroes(matrix [][]int)  {
    m,n:=len(matrix), len(matrix[0])
    tx := make([]int,m)
    ty := make([]int,n)

    for x :=0;x < m;x++{
        for y := 0;y < n;y++{
            if matrix[x][y] == 0{
                tx[x] = 1
                ty[y] = 1
            }
        }
    }

    for x :=0;x < len(matrix);x++{
        for y := 0;y <len(matrix[0]);y++{
            if tx[x] == 1 || ty[y] == 1 {
                matrix[x][y] = 0
            }
        }
    }
}
```
