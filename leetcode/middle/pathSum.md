##  路径总和 II

给定一个二叉树和一个目标和，找到所有从根节点到叶子节点路径总和等于给定目标和的路径。

说明: 叶子节点是指没有子节点的节点。

示例:
给定如下二叉树，以及目标和 sum = 22，

              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
返回:

[
   [5,4,11,2],
   [5,8,4,5]
]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/path-sum-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//用go回溯很容易出现问题. 主要在go在数组上的处理不是函数式编程的形式
func pathSum(root *TreeNode, sum int) [][]int {

	if root == nil{
		return nil
	}

	ans := make([][]int, 0)
	cur := []int{}
	var backtrace func( root *TreeNode, sum int)
	backtrace = func(root *TreeNode, sum int) {
		if root == nil{
			return
		}


		if sum == root.Val && root.Left == nil && root.Right == nil{
			ans = append(ans,append([]int{},append(cur,root.Val)...))
			return
		}

		cur  = append(cur,root.Val)

		backtrace(root.Left,sum-root.Val)
		backtrace(root.Right,sum-root.Val)
		cur = cur[:len(cur) -1]
	}

	backtrace(root,sum)
	return ans

}


```
