## 填充每个节点的下一个右侧节点指针 II

给定一个二叉树

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL。

初始状态下，所有 next 指针都被设置为 NULL。

 

进阶：

你只能使用常量级额外空间。
使用递归解题也符合要求，本题中递归程序占用的栈空间不算做额外的空间复杂度。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/populating-next-right-pointers-in-each-node-ii
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func connect(root *Node) *Node {
	if root == nil{
		return nil
	}

	cur := []*Node{root}

	for len(cur) >0 {
		queue:= len(cur)

		for queue>0{
			queue --
			if cur[0].Left != nil{
				cur = append(cur,cur[0].Left)
			}
			if cur[0].Right != nil{
				cur = append(cur,cur[0].Right)
			}
		
            if queue ==0{
                cur[0].Next = nil
            }else{
                cur[0].Next =cur[1]			    
            }
			cur =cur[1:]
		}
	}
	return root
}
//使用空间为常量
func connect(root *Node) *Node {
	if root == nil{
		return nil
	}

    cLink := root
	for cLink != nil {
        var head *Node
        var pre * Node 
		for cLink != nil{
			
			if cLink.Left != nil{
                if head != nil{
                    head.Next =cLink.Left
                }else{
                    pre =cLink.Left
                }
                head = cLink.Left
			}

			
			if cLink.Right != nil{
                if head != nil{
                    head.Next =cLink.Right
                }else{
                    pre =cLink.Right
                }
                head = cLink.Right
			}
		
			cLink=cLink.Next
		}
        cLink =pre
	}
	return root
}
```
