## 相交链表

编写一个程序，找到两个单链表相交的起始节点。

```go
//暴力破解法  时间O(mn) 空间O(1)
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
//拼接 时间O(M+N) 时间O(1)
func getIntersectionNode(headA, headB *ListNode) *ListNode {

    
    tailA := headA
    tailB := headB
    for tailA != tailB  {
       
        if tailA == nil{
            tailA = headB
        }else{
            tailA = tailA.Next
        }
        
        if tailB == nil{
            tailB = headA
        }else{
            tailB = tailB.Next
        }
	}
    return tailA
    
}

```
