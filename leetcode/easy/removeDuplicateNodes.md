## 移除重复节点

编写代码，移除未排序链表中的重复节点。保留最开始出现的节点。

示例1:

 输入：[1, 2, 3, 3, 2, 1]
 输出：[1, 2, 3]
示例2:

 输入：[1, 1, 1, 1, 2]
 输出：[1, 2]
提示：

链表长度在[0, 20000]范围内。
链表元素在[0, 20000]范围内。
进阶：

如果不得使用临时缓冲区，该怎么解决？

```go
func removeDuplicateNodes(head *ListNode) *ListNode {
    
    if head ==  nil{
        return nil
    }

    rep := head
    maps := make(map[int]int)
    maps[head.Val] = 1
    for head != nil && head.Next != nil{
        if maps[head.Next.Val] == 1{
            head.Next = head.Next.Next
        }else{
            maps[head.Next.Val] += 1            
            head = head.Next
        }
    }
    return rep

}
```
