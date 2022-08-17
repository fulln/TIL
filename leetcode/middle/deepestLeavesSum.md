层数最深叶子节点的和


给你一棵二叉树的根节点 root ，请你返回 层数最深的叶子节点的和 。

 

示例 1：



输入：root = [1,2,3,4,5,null,6,7,null,null,null,null,8]
输出：15
示例 2：

输入：root = [6,7,8,2,7,1,3,9,null,1,4,null,null,null,5]
输出：19
 

提示：

树中节点数目在范围 [1, 104] 之间。
1 <= Node.val <= 100

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/deepest-leaves-sum
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



func deepestLeavesSum(root *TreeNode) int {
    maxs,index := 0 ,0
    var dfs func(rt *TreeNode,i int)
    dfs = func(rt *TreeNode,i int){
        if rt == nil{
            return;
        }
        if i > index {
            index = i
            maxs = rt.Val
        }else if i == index{
            maxs += rt.Val
        }
        dfs(rt.Left,i+1)
        dfs(rt.Right,i+1)
    }
    dfs(root,0)
    return maxs

}

```
