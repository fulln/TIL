## 二叉搜索树中第K小的元素
给定一个二叉搜索树，编写一个函数 kthSmallest 来查找其中第 k 个最小的元素。

说明：
你可以假设 k 总是有效的，1 ≤ k ≤ 二叉搜索树元素个数。

示例 1:

输入: root = [3,1,4,null,2], k = 1
   3
  / \
 1   4
  \
   2
输出: 1
示例 2:

输入: root = [5,3,6,2,4,null,null,1], k = 3
       5
      / \
     3   6
    / \
   2   4
  /
 1
输出: 3
进阶：
如果二叉搜索树经常被修改（插入/删除操作）并且你需要频繁地查找第 k 小的值，你将如何优化 kthSmallest 函数？

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvuyv3/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func kthSmallest(root *TreeNode, k int) int {
   //后续递归遍历
    stru := dg(root,k)
    return stru[k-1]
}
func dg(root *TreeNode,k int) []int{
   returns := []int{}
   if root ==  nil{
       return returns
   }
   
   returns =append(returns,dg(root.Left,k)...)
   
   if len(returns) >= k{
       return returns
   }
   returns = append(returns,root.Val)
   if len(returns) >= k{
       return returns
   }
   returns =append(returns,dg(root.Right,k)...)
   
   return returns
}

func kthSmallest(root *TreeNode, k int) int {
    returns := []*TreeNode{}

    for{

        for root != nil{
            returns = append(returns,root)
            root = root.Left
        }

        now := returns[len(returns) -1]
        
        returns = returns[:len(returns) -1]

        k -= 1

        if k == 0{
            return now.Val
        }

        root = now.Right

    }

}
```
