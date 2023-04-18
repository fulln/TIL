#算法 #数据结构 #二叉树 #leetcode 

#### [1026. 节点与其祖先之间的最大差值](https://leetcode.cn/problems/maximum-difference-between-node-and-ancestor/)

给定二叉树的根节点 root，找出存在于 不同 节点 A 和 B 之间的最大值 V，其中 V = |A.val - B.val|，且 A 是 B 的祖先。

（如果 A 的任何子节点之一为 B，或者 A 的任何子节点是 B 的祖先，那么我们认为 A 是 B 的祖先）

 

示例 1：



输入：root = [8,3,10,1,6,null,14,null,null,4,7,13]
输出：7
解释： 
我们有大量的节点与其祖先的差值，其中一些如下：
|8 - 3| = 5
|3 - 7| = 4
|8 - 1| = 7
|10 - 13| = 3
在所有可能的差值中，最大值 7 由 |8 - 1| = 7 得出。
示例 2：


输入：root = [1,null,2,null,0,3]
输出：3
 

提示：

树中的节点数在 2 到 5000 之间。
0 <= Node.val <= 105

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-difference-between-node-and-ancestor
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
/**

 * Definition for a binary tree node.

 * type TreeNode struct {

 *     Val int

 *     Left *TreeNode

 *     Right *TreeNode

 * }

 */

func maxAncestorDiff(root *TreeNode) int {

    var current = 0

    var dfs func(root *TreeNode,max,min int)

  

    dfs=func(root *TreeNode,max,min int){

        if root == nil{

            return 

        }

        max = maxNum(max,root.Val)

        min = minNum(min,root.Val)

  

        current = maxNum(current,maxNum(max-root.Val,root.Val-min))

        dfs(root.Left,max,min)

        dfs(root.Right,max,min)

    }

  

    dfs(root,root.Val,root.Val)

  

    return current

}

  

func maxNum(a,b int)int{

    if a > b{

        return a 

    }else{

        return b

    }

}

  

func minNum(a,b int)int{

    if a < b{

        return a 

    }else{

        return b

    }

}
```