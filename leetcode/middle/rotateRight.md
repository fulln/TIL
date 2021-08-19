## 旋转链表
给你一个链表的头节点 head ，旋转链表，将链表每个节点向右移动 k 个位置。

 

示例 1：


输入：head = [1,2,3,4,5], k = 2
输出：[4,5,1,2,3]
示例 2：


输入：head = [0,1,2], k = 4
输出：[2,0,1]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/rotate-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func rotateRight(head *ListNode, k int) *ListNode {
    if head ==nil || head.Next == nil ||k ==0{
        return head
    }
    
    count := 1

    tmp := head
    for tmp.Next != nil{
        tmp =tmp.Next
        count ++
    }

    k %=  count

    if k == 0{
        return head
    }

    tmp.Next = head

    for i:=0;i< count - k;i++{
        tmp =tmp.Next
    }
    head ,tmp.Next =tmp.Next,nil
    return head
}
```
