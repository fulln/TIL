## 统计值等于子树平均值的节点数
6057. 统计值等于子树平均值的节点数 显示英文描述 
通过的用户数4565
尝试过的用户数4688
用户总通过次数4628
用户总提交次数5525
题目难度Medium
给你一棵二叉树的根节点 root ，找出并返回满足要求的节点数，要求节点的值等于其 子树 中值的 平均值 。

注意：

n 个元素的平均值可以由 n 个元素 求和 然后再除以 n ，并 向下舍入 到最近的整数。
root 的 子树 由 root 和它的所有后代组成。
 

示例 1：


输入：root = [4,8,5,0,1,null,6]
输出：5
解释：
对值为 4 的节点：子树的平均值 (4 + 8 + 5 + 0 + 1 + 6) / 6 = 24 / 6 = 4 。
对值为 5 的节点：子树的平均值 (5 + 6) / 2 = 11 / 2 = 5 。
对值为 0 的节点：子树的平均值 0 / 1 = 0 。
对值为 1 的节点：子树的平均值 1 / 1 = 1 。
对值为 6 的节点：子树的平均值 6 / 1 = 6 。
示例 2：


输入：root = [1]
输出：1
解释：对值为 1 的节点：子树的平均值 1 / 1 = 1
```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func averageOfSubtree(root *TreeNode) int {
    avg := 0
    
    var dfs func(curr *TreeNode)(int,int)
    
    dfs = func(curr *TreeNode)(int,int){
        if curr ==  nil{
            return 0,0
        }
        lsum,lc := dfs(curr.Left)
        rsum,rc := dfs(curr.Right)
        
        csum := lsum + rsum + curr.Val
        cls :=  lc + rc + 1
        
        if csum  / cls == curr.Val {
            avg +=1
        }  
        
        return csum,cls 
    }
    
    dfs(root)
    
    return avg
    
}
```
