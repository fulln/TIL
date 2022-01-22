## 叶子相似的树
请考虑一棵二叉树上所有的叶子，这些叶子的值按从左到右的顺序排列形成一个 叶值序列 。



举个例子，如上图所示，给定一棵叶值序列为 (6, 7, 4, 9, 8) 的树。

如果有两棵二叉树的叶值序列是相同，那么我们就认为它们是 叶相似 的。

如果给定的两个根结点分别为 root1 和 root2 的树是叶相似的，则返回 true；否则返回 false 。

 

示例 1：



输入：root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]
输出：true
示例 2：

输入：root1 = [1], root2 = [1]
输出：true
示例 3：

输入：root1 = [1], root2 = [2]
输出：false
示例 4：

输入：root1 = [1,2], root2 = [2,2]
输出：true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/leaf-similar-trees
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
func leafSimilar(root1 *TreeNode, root2 *TreeNode) bool {
    val1 := before(root1) 
    val2 := before(root2)

    if len(val1) != len(val2){
        return false
    }
    
    for i:=0;i< len(val1);i++{
        if val1[i] != val2[i]{
            return false
        }
    } 
    return true

}

func before(root *TreeNode)[]int{

    if root == nil{
        return nil
    }

    ret:= []int{}

    if root.Left == nil && root.Right == nil  {
        ret = append(ret,root.Val)
    }else{
        val1 :=before(root.Left)
        val2 := before(root.Right)

        ret =append(ret, val1...) 
        ret =append(ret,val2...)
    }

    return ret
}
```
