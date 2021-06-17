##  队列的最大值
请定义一个队列并实现函数 max_value 得到队列里的最大值，要求函数max_value、push_back 和 pop_front 的均摊时间复杂度都是O(1)。

若队列为空，pop_front 和 max_value 需要返回 -1

示例 1：

输入: 
["MaxQueue","push_back","push_back","max_value","pop_front","max_value"]
[[],[1],[2],[],[],[]]
输出: [null,null,null,2,1,2]
示例 2：

输入: 
["MaxQueue","pop_front","max_value"]
[[],[],[]]
输出: [null,-1,-1]
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/dui-lie-de-zui-da-zhi-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
type MaxQueue struct {
    queue []int
    dequeue []int
}


func Constructor() MaxQueue {
    return MaxQueue{}
}


func (this *MaxQueue) Max_value() int {
    if len(this.queue) == 0{
        return -1
    }
    return this.dequeue[0]
}


func (this *MaxQueue) Push_back(value int)  {
    this.queue = append(this.queue,value)
    for len(this.dequeue) > 0  && this.dequeue[len(this.dequeue) -1] < value{
       this.dequeue = this.dequeue[:len(this.dequeue) -1]
    }
    this.dequeue = append(this.dequeue,value)
}


func (this *MaxQueue) Pop_front() int {
      if len(this.queue) == 0 {
        return -1
    }
    if this.queue[0] == this.dequeue[0] {
        this.dequeue = this.dequeue[1: ]
    }
    value := this.queue[0]
    this.queue = this.queue[1: ]
    return value
}


/**
 * Your MaxQueue object will be instantiated and called as such:
 * obj := Constructor();
 * param_1 := obj.Max_value();
 * obj.Push_back(value);
 * param_3 := obj.Pop_front();
 */
```
