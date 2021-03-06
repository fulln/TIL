##  二叉树的中序遍历
给定一个二叉树，返回它的中序 遍历。

示例:

输入: [1,null,2,3]
   1
    \
     2
    /
   3

输出: [1,3,2]
进阶: 递归算法很简单，你可以通过迭代算法完成吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-inorder-traversal
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
 //递归
func inorderTraversal(root *TreeNode) []int {
    if root ==  nil{
        return nil
    }

    returns := []int{}
    var nodes []int

    nodes = inorderTraversal(root.Left)

    if nodes != nil{
        returns  = append(returns,nodes...)
    }

    returns = append(returns,root.Val)

    nodes = inorderTraversal(root.Right)

    if nodes != nil{
        returns  = append(returns,nodes...)
    }

    return returns

}

 //迭代
func inorderTraversal(root *TreeNode) []int {

    returns  := []int{}
    nodes := []*TreeNode{}
    

    for root != nil || len(nodes) != 0{

        for root != nil{
            nodes = append(nodes,root)
            root = root.Left
        }
        root = nodes[len(nodes) -1]
        nodes = nodes[:len(nodes) -1]
        returns = append(returns,root.Val)
        root = root.Right   
    }

    return returns
}


```
