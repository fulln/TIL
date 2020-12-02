## 验证二叉搜索树

给定一个二叉树，判断其是否是一个有效的二叉搜索树。

假设一个二叉搜索树具有如下特征：

节点的左子树只包含小于当前节点的数。
节点的右子树只包含大于当前节点的数。
所有左子树和右子树自身必须也是二叉搜索树。
示例 1:

输入:
    2
   / \
  1   3
输出: true
示例 2:

输入:
    5
   / \
  1   4
     / \
    3   6
输出: false
解释: 输入为: [5,1,4,null,null,3,6]。
     根节点的值为 5 ，但是其右子节点值为 4 。

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-easy/xn08xg/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```go
func isValidBST(root *TreeNode) bool {
    return valiBST(root,math.MinInt64,math.MaxInt64)
}

func valiBST(root *TreeNode,min,max int)bool{

    if root == nil{
        return true
    }
   // 判断节点的值是不是在区间呢，不是的话就false结束
    if root.Val<=min || root.Val>=max{
        return false
    }

    //左递归 最大值改为当前节点值
    //右递归 最小值改为当前节点值
    return valiBST(root.Left,min,root.Val) && valiBST(root.Right,root.Val,max) 

}
```
