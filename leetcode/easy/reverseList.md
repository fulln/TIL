## 反转链表

反转一个单链表。

示例:

输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
进阶:
你可以迭代或递归地反转链表。你能否用两种方法解决这道题？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
//递归
var(
	begin *ListNode
)
func reverseList(head *ListNode) *ListNode {
    if head == nil{
        return nil
    }
	charge(head)
	return begin.Next
}

func charge(head *ListNode) *ListNode {
    
	if head.Next == nil{
		begin = &ListNode{}
		begin.Next=head
		return head
	}
    
	node := charge(head.Next)
    head.Next = nil
	node.Next = head
	return node.Next
}
//递归(官方)
func reverseList(head *ListNode) *ListNode {
    if head == nil||  head.Next == nil {
		return head
	}
    
	node := reverseList(head.Next)
    head.Next.Next =head
    head.Next = nil   
	return node
}
//迭代

func reverseList(head *ListNode) *ListNode {
 var prev *ListNode
    for head != nil {
        head.Next, head, prev = prev, head.Next, head
    }
    return prev

}



```
