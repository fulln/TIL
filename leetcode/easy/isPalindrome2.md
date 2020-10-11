## 回文链表

请判断一个链表是否为回文链表。

示例 1:

输入: 1->2
输出: false
示例 2:

输入: 1->2->2->1
输出: true
进阶：
你能否用 O(n) 时间复杂度和 O(1) 空间复杂度解决此题？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/palindrome-linked-list
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
 // 时间复杂度  3/2 On  空间复杂度On
func isPalindrome(head *ListNode) bool {
    tmp :=make([]*ListNode,0) 
    
    for head != nil {
        tmp = append(tmp,head)
        head = head.Next     
    }
    
    for from,end :=0,len(tmp) -1;from < end;from,end =  from+1,end -1{
        if tmp[from].Val != tmp[end].Val{
            return false
        }
    }

    return true

}
```
