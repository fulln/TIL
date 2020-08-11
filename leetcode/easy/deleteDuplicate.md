## 删除排序链表中的重复元素

```go
/**
给定一个排序链表，删除所有重复的元素，使得每个元素只出现一次。

示例 1:

输入: 1->1->2
输出: 1->2
示例 2:

输入: 1->1->2->3->3
输出: 1->2->3
*/
func deleteDuplicates(head *ListNode) *ListNode {
var tail = &ListNode{}

	tail.Next = head

	for head.Next != nil {
		if head.Val == head.Next.Val {
			head.Next = head.Next.Next
		} else {
			head = head.Next
		}

	}
	return tail.Next
}
```
