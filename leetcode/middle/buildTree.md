## 从前序与中序遍历序列构造二叉树
根据一棵树的前序遍历与中序遍历构造二叉树。

注意:
你可以假设树中没有重复的元素。

例如，给出

前序遍历 preorder = [3,9,20,15,7]
中序遍历 inorder = [9,3,15,20,7]
返回如下的二叉树：

    3
   / \
  9  20
    /  \
   15   7

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal
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
func buildTree(preorder []int, inorder []int) *TreeNode {

    if len(preorder) == 0{
        return nil
    }

    if len(inorder) == 0{
        return nil
    }

    root := &TreeNode{}

    root.Val = preorder[0]

    var middle int    
    for i:=0;i< len(inorder);i++{
        if inorder[i]  == root.Val{
            middle = i
            break
        }  
    }

    val1 :=  buildTree(preorder[1:middle+1],inorder[0:middle])
    if val1 != nil{
         root.Left =val1
    }


    val2 := buildTree(preorder[middle+1:],inorder[middle+1:])
    if val2 != nil{
         root.Right =val2
    }
    return root
  
}


```
