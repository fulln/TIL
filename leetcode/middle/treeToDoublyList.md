## 剑指 Offer 36. 二叉搜索树与双向链表
输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的循环双向链表。要求不能创建任何新的节点，只能调整树中节点指针的指向。

 

为了让您更好地理解问题，以下面的二叉搜索树为例：

 



 

我们希望将这个二叉搜索树转化为双向循环链表。链表中的每个节点都有一个前驱和后继指针。对于双向循环链表，第一个节点的前驱是最后一个节点，最后一个节点的后继是第一个节点。

下图展示了上面的二叉搜索树转化成的链表。“head” 表示指向链表中有最小元素的节点。

 



 

特别地，我们希望可以就地完成转换操作。当转化完成以后，树中节点的左指针需要指向前驱，树中节点的右指针需要指向后继。还需要返回链表中的第一个节点的指针。

 

注意：本题与主站 426 题相同：https://leetcode-cn.com/problems/convert-binary-search-tree-to-sorted-doubly-linked-list/

注意：此题对比原题有改动。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/er-cha-sou-suo-shu-yu-shuang-xiang-lian-biao-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```java
/*
// Definition for a Node.
class Node {
    public int val;
    public Node left;
    public Node right;

    public Node() {}

    public Node(int _val) {
        val = _val;
    }

    public Node(int _val,Node _left,Node _right) {
        val = _val;
        left = _left;
        right = _right;
    }
};
*/
class Solution {
    public Node treeToDoublyList(Node root) {
            if (root ==  null){
                return null;
            }
            Node curr = root;
            List<Node> ret = new ArrayList<>();
            List<Node> arr = new ArrayList<>();
            //2叉搜索树,中序遍历
            while (curr != null || arr.size() > 0) {
                while (curr != null) {
                    arr.add(curr);
                    curr =curr.left;
                }
                curr = arr.get(arr.size() -1);
                arr.remove(arr.size() -1);
                ret.add(curr);
                curr = curr.right;
            }
            int size = ret.size();
            for (int i = 0; i < size; i++) {
                //修改左边
                if (i == 0) {
                    ret.get(i).left = ret.get(size - 1);
                } else {
                    ret.get(i).left = ret.get(i - 1);
                }
                //修改右边
                if (i == size - 1) {
                    ret.get(i).right = ret.get(0);
                } else {
                    ret.get(i).right = ret.get(i + 1);
                }
            }
            return ret.get(0);
        }
        

  
}
```
