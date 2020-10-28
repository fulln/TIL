## 144. 二叉树的前序遍历

给定一个二叉树，返回它的 前序 遍历。

 示例:

输入: [1,null,2,3]  
   1
    \
     2
    /
   3 

输出: [1,2,3]
进阶: 递归算法很简单，你可以通过迭代算法完成吗？

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
func preorderTraversal(root *TreeNode) []int {
    
    if root ==  nil{
        return []int{}
    }


    returns := append([]int{},root.Val)

    left := preorderTraversal(root.Left)

    returns = append(returns,left...)

    right := preorderTraversal(root.Right)

    return  append(returns,right...)


}
//迭代


```
