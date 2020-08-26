## 环形链表

给定一个链表，判断链表中是否有环。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。

```go
func hasCycle(head *ListNode) bool {
    if head == nil{
        return false
    }
    first  := head.Next
    second := head

    for first != nil && second != nil && first.Next != nil {
       if second.Val == first.Val{
            return true
       } 
        second = second.Next
        first = first.Next.Next
    }
    return false

}
```
