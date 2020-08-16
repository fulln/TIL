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
    var returns = [][]int{}
    if root ==  nil{
        return returns
    }

    left := levelOrderBottom(root.Left)
    right := levelOrderBottom(root.Right)
    
    var index  = []int{}

    index =append(index,root.Val)

    returns = append(returns,index)

    if left == nil && right == nil{
        return returns
    }

    if left == nil {
        return append(right,returns...)
    }

    
    if right == nil {
        return append(left,returns...)
    }


    if len(left) >= len(right){
        for i:=0 ; i <len(left) ;i++{
            if len(right) <i{
                left[i] = append(left[i],right[i]...)        
            }
        }
        return append(left,returns...) 
    }else{
        for i:=0 ; i <len(right) ;i++{
            if len(left) <i{
                right[i] = append(right[i],left[i]...)
            }
        } 
        return append(right,returns...)
    }

}
```
