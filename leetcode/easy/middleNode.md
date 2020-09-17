## 链表的中间结点
给定一个带有头结点 head 的非空单链表，返回链表的中间结点。

如果有两个中间结点，则返回第二个中间结点。

```go
func middleNode(head *ListNode) *ListNode {
    returns := head
    for returns != nil &&returns.Next != nil{
        returns =returns.Next.Next
        head =head.Next
    }
    return head
}

```
