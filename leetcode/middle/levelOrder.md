## 二叉树的层序遍历
给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。

 

示例：
二叉树：[3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回其层次遍历结果：

[
  [3],
  [9,20],
  [15,7]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-level-order-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
// bfs 一次性写出
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func levelOrder(root *TreeNode) [][]int {

    returns := [][]int{}

    if root == nil{
        return returns
    }
    queue := []*TreeNode{root}
    for len(queue) > 0 {
        queuel := len(queue)
        box := []int{}
        for queuel > 0{
            if queue[0].Left != nil{
                queue = append(queue,queue[0].Left)
            }
            
            if queue[0].Right != nil{
                queue = append(queue,queue[0].Right)
            }
            box = append(box,queue[0].Val)
            queue = queue[1:]
            queuel --
        }
        returns = append(returns,box)
    }

    return returns

}
```
