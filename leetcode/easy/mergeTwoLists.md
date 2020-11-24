## 合并两个有序链表

```go

package main

//将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
//
//
//
// 示例：
//
// 输入：1->2->4, 1->3->4
//输出：1->1->2->3->4->4
//
// Related Topics 链表
// 👍 1143 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
/**
* Definition for singly-linked list.
 */

type ListNode struct {
	Val  int
	Next *ListNode
}

func mergeTwoLists3(l1 *ListNode, l2 *ListNode) *ListNode {
	var head = &ListNode{}
	tail := head
	for l1 != nil && l2 != nil {
		if l1.Val > l2.Val {
			tail.Next = l2
			l2 = l2.Next
		} else {
			tail.Next = l1
			l1 = l1.Next
		}
		tail = tail.Next
	}
	if l1 != nil {
		tail.Next = l1
	} else {
		tail.Next = l2
	}
	return head.Next
}

func mergeTwoLists4(l1 *ListNode, l2 *ListNode) *ListNode {
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}

	if l1.Val > l2.Val {
		l2.Next = mergeTwoLists4(l1, l2.Next)
		return l2
	} else {
		l1.Next = mergeTwoLists4(l1.Next, l2)
		return l1
	}

}

func mergeTwoLists(l1 *ListNode, l2 *ListNode) *ListNode {
	var dump = &ListNode{}
	pre := dump
	//迭代
	for l1 != nil && l2 != nil {
		if l1.Val < l2.Val {
			pre.Next = l1
			l1 = l1.Next
		} else {
			pre.Next = l2
			l2 = l2.Next
		}
		pre = pre.Next
	}
	if l1 != nil {
		pre.Next = l1
	} else {
		pre.Next = l2
	}
	return dump.Next
}
func mergeTwoLists2(l1 *ListNode, l2 *ListNode) *ListNode {
	//递归
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}
	if l1.Val < l2.Val {
		l1.Next = mergeTwoLists2(l1.Next, l2)
		return l1
	} else {
		l2.Next = mergeTwoLists2(l1, l2.Next)
		return l2
	}

}

func main() {
	var l1 = new(ListNode)
	var l11 = new(ListNode)
	var l111 = new(ListNode)
	var l2 = new(ListNode)
	var l21 = new(ListNode)
	var l211 = new(ListNode)
	l1.Val = 1
	l11.Val = 2
	l111.Val = 4
	l1.Next = l11
	l11.Next = l111
	l2.Val = 1
	l21.Val = 3
	l211.Val = 4
	l2.Next = l21
	l21.Next = l211

	lists := mergeTwoLists4(l1, l2)
	for lists.Next != nil {

		print(lists.Val)
		lists = lists.Next
	}
	print(lists.Val)

}

//leetcode submit region end(Prohibit modification and deletion)
```
