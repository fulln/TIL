## . 寻找重复的子树

给定一棵二叉树 root，返回所有重复的子树。

对于同一类的重复子树，你只需要返回其中任意一棵的根结点即可。

如果两棵树具有相同的结构和相同的结点值，则它们是重复的。

 

示例 1：



输入：root = [1,2,3,4,null,2,4,null,null,4]
输出：[[2,4],[4]]
示例 2：



输入：root = [2,1,1]
输出：[[1]]
示例 3：



输入：root = [2,2,2,3,null,3,null]
输出：[[2,3],[3]]

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/find-duplicate-subtrees
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

func findDuplicateSubtrees(root *TreeNode) []*TreeNode {
    maps  := map[string]int{}
    strMp := map[string]*TreeNode{}

    var dfs func(root *TreeNode) string
	dfs = func(root *TreeNode) string {
		if root == nil {
			return "|"
		}
		var str string
		str += "." + strconv.Itoa(root.Val)
		str += dfs(root.Left)
		str += dfs(root.Right)
		maps[str]++
		strMp[str] = root
		return str
	}
	dfs(root)
	res := []*TreeNode{}
    for i := range maps {
		if maps[i] > 1 {
			res = append(res, strMp[i])
		}
	}
    return res
}
```
