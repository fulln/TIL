##  输出二叉树

给你一棵二叉树的根节点 root ，请你构造一个下标从 0 开始、大小为 m x n 的字符串矩阵 res ，用以表示树的 格式化布局 。构造此格式化布局矩阵需要遵循以下规则：

树的 高度 为 height ，矩阵的行数 m 应该等于 height + 1 。
矩阵的列数 n 应该等于 2height+1 - 1 。
根节点 需要放置在 顶行 的 正中间 ，对应位置为 res[0][(n-1)/2] 。
对于放置在矩阵中的每个节点，设对应位置为 res[r][c] ，将其左子节点放置在 res[r+1][c-2height-r-1] ，右子节点放置在 res[r+1][c+2height-r-1] 。
继续这一过程，直到树中的所有节点都妥善放置。
任意空单元格都应该包含空字符串 "" 。
返回构造得到的矩阵 res 。

 

 

示例 1：


输入：root = [1,2]
输出：
[["","1",""],
 ["2","",""]]
示例 2：


输入：root = [1,2,3,null,4]
输出：
[["","","","1","","",""],
 ["","2","","","","3",""],
 ["","","4","","","",""]]
 

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/print-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
 type node struct {
    root *TreeNode
    x int
}

func printTree(root *TreeNode) [][]string {
    if root == nil {
        return [][]string{}
    }
    var maxHeight, n = 0, 0
    var dfs func(root *TreeNode, h int) int
    dfs = func(root *TreeNode, h int) int {
        if root == nil {
            return h
        }
        var vh = h
        vh = max(vh, dfs(root.Left, h))
        vh = max(vh, dfs(root.Right, h))
        return vh+1
    }
    maxHeight = dfs(root, 0)-1
    n = int(math.Pow(2,float64(maxHeight+1)))-1
    q := make([]*node, 0)
    q = append(q, &node{root, (n-1)/2})
    res := make([][]string, 0, maxHeight+1)
    h := 0
    for len(q) > 0 {
        size := len(q)
        curRow := make([]string, n)
        for size > 0 {
            size--
            cur := q[0]
            q = q[1:]
            curRow[cur.x] = strconv.Itoa(cur.root.Val)
            if cur.root.Left != nil {
                q = append(q, &node{cur.root.Left, cur.x-int(math.Pow(2,float64(maxHeight-h-1)))})
            }
            if cur.root.Right != nil {
                q = append(q, &node{cur.root.Right, cur.x+int(math.Pow(2,float64(maxHeight-h-1)))})
            }
        }
        res = append(res, curRow)
        h++
    }
    return res
}

func max(a, b int) int {
    if a < b {
        return b
    }
    return a
}

```
