---
dg-publish: true
title: All Nodes Distance K in Binary Tree
createTime: 2023-07-11 23:57  
---
#leetcode  #middle 

# All Nodes Distance K in Binary Tree

Given the `root` of a binary tree, the value of a target node `target`, and an integer `k`, return _an array of the values of all nodes that have a distance_ `k` _from the target node._

You can return the answer in **any order**.

**Example 1:**

![](https://s3-lc-upload.s3.amazonaws.com/uploads/2018/06/28/sketch0.png)

**Input:** root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2
**Output:** [7,4,1]
Explanation: The nodes that are a distance 2 from the target node (with value 5) have values 7, 4, and 1.

**Example 2:**

**Input:** root = [1], target = 1, k = 3
**Output:** []

**Constraints:**

- The number of nodes in the tree is in the range `[1, 500]`.
- `0 <= Node.val <= 500`
- All the values `Node.val` are **unique**.
- `target` is the value of one of the nodes in the tree.
- `0 <= k <= 1000`

```java
/**

 * Definition for a binary tree node.

 * type TreeNode struct {

 *     Val int

 *     Left *TreeNode

 *     Right *TreeNode

 * }

 */

public void getParentsByDFS(Map<TreeNode, TreeNode> parent, TreeNode root) {  
if (root == null)  
return;  
if (root.left != null)  
parent.put(root.left, root);  
if (root.right != null)  
parent.put(root.right, root);  
getParentsByDFS(parent, root.left);  
getParentsByDFS(parent, root.right);  
}  
  
public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {  
Map<TreeNode, TreeNode> parent = new HashMap<>();  
getParentsByDFS(parent, root);  
Queue<TreeNode> queue = new LinkedList<>();  
Map<TreeNode, Boolean> visited = new HashMap<>();  
visited.put(target, true);  
queue.offer(target);  
int level = 0;  
while (!queue.isEmpty()) {  
int n = queue.size();  
if (level == k)  
break;  
level++;  
while (n-- > 0) {  
TreeNode curr = queue.poll();  
if (curr.left != null && !visited.containsKey(curr.left)) {  
visited.put(curr.left, true);  
queue.offer(curr.left);  
}  
if (curr.right != null && !visited.containsKey(curr.right)) {  
visited.put(curr.right, true);  
queue.offer(curr.right);  
}  
if (parent.containsKey(curr) && !visited.containsKey(parent.get(curr))) {  
visited.put(parent.get(curr), true);  
queue.offer(parent.get(curr));  
}  
}  
}  
List<Integer> ans = new ArrayList<>();  
while (!queue.isEmpty()) {  
ans.add(queue.poll().val);  
}  
return ans;  
}  
}
```
