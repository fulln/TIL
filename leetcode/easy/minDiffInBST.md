##  二叉搜索树节点最小距离
给你一个二叉搜索树的根节点 root ，返回 树中任意两不同节点值之间的最小差值 。

注意：本题与 530：https://leetcode-cn.com/problems/minimum-absolute-difference-in-bst/ 相同

 

示例 1：


输入：root = [4,2,6,1,3]
输出：1
示例 2：


输入：root = [1,0,48,null,null,12,49]
输出：1

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-distance-between-bst-nodes
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
func minDiffInBST(root *TreeNode) int {
    if root == nil{
        return 0
    }

    small :=100000
    lastNode := small;
    var before func(root *TreeNode)
    //2叉树中序遍历
    before = func(root *TreeNode){
        if root ==  nil{
            return
        }
        before(root.Left)
        if lastNode != small  && root.Val - lastNode < small{
            small = root.Val - lastNode
        }
        lastNode = root.Val 
        before(root.Right)

    } 

    before(root)

    return small

}
```
