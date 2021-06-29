## 二叉树染色

小扣有一个根结点为 root 的二叉树模型，初始所有结点均为白色，可以用蓝色染料给模型结点染色，模型的每个结点有一个 val 价值。小扣出于美观考虑，希望最后二叉树上每个蓝色相连部分的结点个数不能超过 k 个，求所有染成蓝色的结点价值总和最大是多少？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-shu-ran-se-UGC
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
func maxValue(root *TreeNode, k int) int {
    dp := make(map[*TreeNode][]int)

    var dfs func(node *TreeNode,left int)int

    dfs = func(node *TreeNode, left int)int{
        if nil == node {
            return  0
        }
        if dp[node] == nil{
            dp[node] = make([]int,k+1)
        } 
        if dp[node][left] > 0{
            return dp[node][left]
        }   
        total:= dfs(node.Left,k) +dfs(node.Right,k)

        for i:=0;i< left;i++{
            total = Max(total,node.Val + dfs(node.Left,i) + dfs(node.Right,left-i-1))
        }
        dp[node][left] = total
        return total
    }
    return dfs(root,k)
}

func Max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
```
