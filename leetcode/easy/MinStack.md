## 最小栈

设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。

push(x) —— 将元素 x 推入栈中。
pop() —— 删除栈顶的元素。
top() —— 获取栈顶元素。
getMin() —— 检索栈中的最小元素。

```go
type MinStack struct {
    middle []int
    mins []int
}


/** initialize your data structure here. */
func Constructor() MinStack {
        return MinStack{
                middle: []int{},
                mins: []int{math.MaxInt64},  
        }
}


func (this *MinStack) Push(x int)  {
    this.middle = append(this.middle,x)
    top := this.mins[len(this.mins) -1]
    this.mins = append(this.mins,min(x,top))
}


func (this *MinStack) Pop()  {
    this.middle = this.middle[:len(this.middle) -1]
    this.mins =this.mins[:len(this.mins) -1]
}


func (this *MinStack) Top() int {
    return this.middle[len(this.middle) -1]

}


func (this *MinStack) GetMin() int {
  return this.mins[len(this.mins) -1]
}

func min(a,b int)int{
    if a >b{
        return b
    }else{
        return a
    }
}
```
