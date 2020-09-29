## 二叉树的后序遍历

给定一个二叉树，返回它的 后序 遍历。

示例:

输入: [1,null,2,3]  
   1
    \
     2
    /
   3 

输出: [3,2,1]
进阶: 递归算法很简单，你可以通过迭代算法完成吗？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/binary-tree-postorder-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//递归
func postorderTraversal(root *TreeNode) []int {

    if root == nil{
        return nil
    }

    returns := make([]int,0)    
    
    left := postorderTraversal(root.Left)
    if left != nil{
        returns  = append(returns,left...) 
    }
        
    right := postorderTraversal(root.Right)
    if right != nil{
        returns = append(returns,right...)
    }

    return append(returns,root.Val)


}

//迭代


```
