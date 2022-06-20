## 508. 出现次数最多的子树元素和

给你一个二叉树的根结点 root ，请返回出现次数最多的子树元素和。如果有多个元素出现的次数相同，返回所有出现次数最多的子树元素和（不限顺序）。

一个结点的 「子树元素和」 定义为以该结点为根的二叉树上所有结点的元素之和（包括结点本身）。

 

示例 1：



输入: root = [5,2,-3]
输出: [2,-3,4]
示例 2：



输入: root = [5,2,-5]
输出: [2]


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/most-frequent-subtree-sum
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
func findFrequentTreeSum(root *TreeNode) []int {
    
    maps := make(map[int]int)
    max := 0

    var dfs func(root *TreeNode)int
     dfs = func(root *TreeNode)int{
        if root == nil  {
            return 0
        }

        l := dfs(root.Left)
        r := dfs(root.Right)
        sum := root.Val
        maps[sum+l+r] ++
        if max < maps[sum+l+r]{
            max = maps[sum+l+r]
        } 
        return sum + l + r
    }

    dfs(root)   
    ret := []int{}
    for k,val := range maps{
        if val == max{
            ret = append(ret,k)
        }
    }
    return ret

    
}
```
