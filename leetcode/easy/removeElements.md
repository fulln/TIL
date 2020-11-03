## 203. 移除链表元素

删除链表中等于给定值 val 的所有节点。

示例:

输入: 1->2->6->3->4->5->6, val = 6
输出: 1->2->3->4->5

```go
func removeElements(head *ListNode, val int) *ListNode {

    for head != nil && head.Val == val{
        head =head.Next
    }

    returuns := &ListNode{
        Val:0,
        Next:head,
    }

    returuns.Next =head

    for  head != nil{
        if head.Next!= nil && head.Next.Val == val {
            head.Next =head.Next.Next       
        }else{
            head =head.Next
        }
    }
    return returuns.Next
}
```
