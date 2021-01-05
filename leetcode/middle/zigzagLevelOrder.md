## 二叉树的锯齿形层次遍历

给定一个二叉树，返回其节点值的锯齿形层序遍历。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。

例如：
给定二叉树 [3,9,20,null,null,15,7],

    3
   / \
  9  20
    /  \
   15   7
返回锯齿形层序遍历如下：

[
  [3],
  [20,9],
  [15,7]
]
相关标签

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvle7s/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func zigzagLevelOrder(root *TreeNode) [][]int {

    returns := [][]int{}

    if root == nil{
        return returns
    }
    queue := []*TreeNode{root}

    for i :=0;len(queue) >0;i++{
        check := []int{}
        nows := queue
        queue = nil
        for _,node := range nows{
            check =append(check,node.Val)
            if node.Left != nil{
                queue = append(queue,node.Left)
            }

            if node.Right != nil{
                queue = append(queue,node.Right)
            }
        }

        if i & 1 ==1 {
            for from,end := 0,len(check)-1;from <end;from,end = from+1,end -1{
                check[from],check[end] = check[end],check[from]
            }
        }

        returns = append(returns,check)

    }
   
    return returns

}
```
