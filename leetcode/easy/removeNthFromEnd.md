## 删除链表的倒数第N个节点

给定一个链表，删除链表的倒数第 n 个节点，并且返回链表的头结点。

示例：

给定一个链表: 1->2->3->4->5, 和 n = 2.

当删除了倒数第二个节点后，链表变为 1->2->3->5.
说明：

给定的 n 保证是有效的。

进阶：

你能尝试使用一趟扫描实现吗？

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-easy/xn2925/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```go
func removeNthFromEnd(head *ListNode, n int) *ListNode {
    

    returns := &ListNode{
        Next:head,
    }

    fast,slow := returns,returns

   for i:=0;i<n;i++{
        fast = fast.Next
    }

    for fast.Next != nil{
        fast =fast.Next
        slow =slow.Next
    }
    
    slow.Next = slow.Next.Next

    return returns.Next

}
```
