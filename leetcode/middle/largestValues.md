## 在每个树行中找最大值
给定一棵二叉树的根节点 root ，请找出该二叉树中每一层的最大值。

 

示例1：



输入: root = [1,3,2,5,3,null,9]
输出: [1,3,9]
示例2：

输入: root = [1,2,3]
输出: [1,3]
 

提示：

二叉树的节点个数的范围是 [0,104]
-231 <= Node.val <= 231 - 1

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/find-largest-value-in-each-tree-row
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
func largestValues(root *TreeNode) []int {
    ans := []int{}
    var dfs func(i int,root *TreeNode)
    dfs = func(i int,root *TreeNode){
        if root == nil{
            return 
        }
        if len(ans) <= i{
            ans =append(ans,root.Val)
        }else if ans[i] < root.Val{
            ans[i] = root.Val
        }
        
        dfs(i+1,root.Left)
        dfs(i+1,root.Right)

    }

    dfs(0,root)
    return ans
}
```
