## 二叉树的层次遍历II

```go
/**
 *
 给定一个二叉树，返回其节点值自底向上的层次遍历。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）

例如：
给定二叉树 [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回其自底向上的层次遍历为：

[
  [15,7],
  [9,20],
  [3]
]

 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func levelOrderBottom(root *TreeNode) [][]int {
        res := [][]int{}
    if root == nil{
        return res
    }
    var queue = []*TreeNode{root}

    for len(queue) > 0 {
        queueLen := len(queue)
        res = append([][]int{[]int{}},res...) // 头插当前层遍历结果
        for queueLen > 0 {
            queueLen--
            if queue[0].Left != nil {
                queue = append(queue, queue[0].Left)
            }
            if queue[0].Right != nil {
                queue = append(queue, queue[0].Right)
            }
            res[0] = append(res[0], queue[0].Val)
            queue = queue[1:]
        }
    }
    return res
}
```
