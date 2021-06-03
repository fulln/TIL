## 最深叶节点的最近公共祖先

给你一个有根节点的二叉树，找到它最深的叶节点的最近公共祖先。

回想一下：

叶节点 是二叉树中没有子节点的节点
树的根节点的 深度 为 0，如果某一节点的深度为 d，那它的子节点的深度就是 d+1
如果我们假定 A 是一组节点 S 的 最近公共祖先，S 中的每个节点都在以 A 为根节点的子树中，且 A 的深度达到此条件下可能的最大值。
 

注意：本题与力扣 865 重复：https://leetcode-cn.com/problems/smallest-subtree-with-all-the-deepest-nodes/

 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lowest-common-ancestor-of-deepest-leaves
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
func lcaDeepestLeaves(root *TreeNode) *TreeNode {
	ret, _ := dfs(root, 0)
	return ret
}

/**
这里返回的是以root为根节点的树的最深深度叶子节点的LCA，以及最大深度
 */
func dfs(root *TreeNode, fromDepth int) (leafLcaNode *TreeNode, finalDepth int) {
	if nil == root {
		return root, fromDepth
	}
	lNode, lDep := dfs(root.Left, fromDepth + 1)
	rNode, rDep := dfs(root.Right, fromDepth + 1)
	if lDep == rDep {
		return root, lDep
	}
	if lDep > rDep {
		return lNode, lDep
	}
	return rNode, rDep
}
```
