## 二叉搜索树中的众数

给定一个有相同值的二叉搜索树（BST），找出 BST 中的所有众数（出现频率最高的元素）。

假定 BST 有如下定义：

结点左子树中所含结点的值小于等于当前结点的值
结点右子树中所含结点的值大于等于当前结点的值
左子树和右子树都是二叉搜索树
例如：
给定 BST [1,null,2,2],



来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-mode-in-binary-search-tree
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

func findMode(root *TreeNode) []int {
    //先用中序遍历到一个数组中,
    //再遍历数组
    //迭代

    answer := []int{}

    var base, count, maxCount int

    update := func(x int) {
        if x == base {
            count++
        } else {
            base, count = x, 1
        }
        if count == maxCount {
            answer = append(answer, base)
        } else if count > maxCount {
            maxCount = count
            answer = []int{base}
        }
    }

    nodes := []*TreeNode{}
    for root != nil || len(nodes) != 0{
        for root != nil{
            nodes = append(nodes,root)
            root =root.Left
        }

        root = nodes[len(nodes) -1]
        nodes= nodes[:len(nodes) -1]
        update(root.Val)
        root = root.Right
    }

    if len(answer) == 0{
        return answer
    }
    
    return answer


    

}
```
