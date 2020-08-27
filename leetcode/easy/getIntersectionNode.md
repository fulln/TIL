## 相交链表

编写一个程序，找到两个单链表相交的起始节点。

```go

func getIntersectionNode(headA, headB *ListNode) *ListNode {

    tailA := headA
    tailB := headB

    for tailA != nil {
		for tailB != nil{
            if tailA == tailB{
                return tailB
            }
            tailB = tailB.Next
        }
       tailA = tailA.Next
       tailB = headB
	}
    return nil
    
}
```
