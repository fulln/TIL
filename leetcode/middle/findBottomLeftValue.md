## 找树左下角的值
给定一个二叉树的 根节点 root，请找出该二叉树的 最底层 最左边 节点的值。

假设二叉树中至少有一个节点。

 

示例 1:



输入: root = [2,1,3]
输出: 1
示例 2:



输入: [1,2,3,4,null,5,6,null,null,7]
输出: 7
 

提示:

二叉树的节点个数的范围是 [1,104]
-231 <= Node.val <= 231 - 1 


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/find-bottom-left-tree-value
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
func findBottomLeftValue(root *TreeNode) int {
    max := -1
    maps := make(map[int]int)
    var dfs func(i int,node *TreeNode)
    dfs = func(i int,node *TreeNode){
        if node == nil{
            return 
        }
        if i > max {
            max = i
            if maps[i] == 0{
                maps[i] = node.Val
            }
        }
        dfs(i+1,node.Left)
        dfs(i+1,node.Right)
    }

    dfs(0,root)

    return maps[max]

}
```
