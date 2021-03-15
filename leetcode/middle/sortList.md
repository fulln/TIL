## 排序链表

给你链表的头结点 head ，请将其按 升序 排列并返回 排序后的链表 。

进阶：

你可以在 O(n log n) 时间复杂度和常数级空间复杂度下，对链表进行排序吗？
 

示例 1：


输入：head = [4,2,1,3]
输出：[1,2,3,4]
示例 2：


输入：head = [-1,5,3,4,0]
输出：[-1,0,3,4,5]
示例 3：

输入：head = []
输出：[]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/xa262d/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func sortList(head *ListNode) *ListNode {
   // 如果 head为空或者head就一位,直接返回
	if head == nil || head.Next == nil {
		return head
	}
    slow,fast := head,head
	for fast != nil && fast.Next != nil && fast.Next.Next != nil {
		slow,fast = slow.Next,fast.Next.Next
	}
    // 把链表拆分成两段,所以设置中间位置即慢指针的next为nil
	n := slow.Next
	slow.Next = nil
	// 递归排序
	return merge(sortList(head),sortList(n))
}

func merge(node1 ,node2 *ListNode)*ListNode{
    node := &ListNode{Val:0}
    current := node
   // 挨个比较俩链表的值,把小的值放到新定义的链表里,排好序
	for node1 != nil && node2 != nil {
		if node1.Val <= node2.Val {
			current.Next,node1 = node1,node1.Next
		} else {
			current.Next,node2 = node2,node2.Next
		}
		current = current.Next
	}

	// 两链表可能有一个没走完,所以要把没走完的放到链表的后面
	// 注意,此处跟 数组不一样的是, 数组为什么要循环,因为数组可能一个数组全部走了(比如 12345与6789比较, 前面的全部走完,后面一个没走),另一个可能有多个没走..
	// 链表虽然也有这种可能,但是 node1和node2已经是有序的了,如果另外一个没有走完,直接把next指向node1或者node2就行,因为这是链表
	if node1 != nil {
		current.Next,node1 = node1,node1.Next
	}
	if node2 != nil {
		current.Next,node2 = node2,node2.Next
	}
	return node.Next

}

```
