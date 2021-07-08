## 从中序与后序遍历序列构造二叉树

根据一棵树的中序遍历与后序遍历构造二叉树。

注意:
你可以假设树中没有重复的元素。

例如，给出

中序遍历 inorder = [9,3,15,20,7]
后序遍历 postorder = [9,15,7,20,3]
返回如下的二叉树：

    3
   / \
  9  20
    /  \
   15   7

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```

func buildTreeAfter( inorder []int,postorder []int) *TreeNode {
	if len(postorder) == 0 {
		return nil
	}

	if len(inorder) == 0 {
		return nil
	}

	root := &TreeNode{}
	root.Val = postorder[len(postorder)-1]
	middle := 0
	for key, id := range inorder {
		if id == root.Val {
			middle = key
			break
		}
	}

	left := buildTreeAfter( inorder[:middle],postorder[:middle])
	if left != nil {
		root.Left = left
	}
	right := buildTreeAfter( inorder[middle+1:],postorder[middle:len(postorder)-1])
	if right != nil {
		root.Right = right
	}
	return root
}

```
