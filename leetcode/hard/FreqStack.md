## 最大频率栈
设计一个类似堆栈的数据结构，将元素推入堆栈，并从堆栈中弹出出现频率最高的元素。

实现 FreqStack 类:

FreqStack() 构造一个空的堆栈。
void push(int val) 将一个整数 val 压入栈顶。
int pop() 删除并返回堆栈中出现频率最高的元素。
如果出现频率最高的元素不只一个，则移除并返回最接近栈顶的元素。
 

示例 1：

输入：
["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"],
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]
输出：[null,null,null,null,null,null,null,5,7,5,4]
解释：
FreqStack = new FreqStack();
freqStack.push (5);//堆栈为 [5]
freqStack.push (7);//堆栈是 [5,7]
freqStack.push (5);//堆栈是 [5,7,5]
freqStack.push (7);//堆栈是 [5,7,5,7]
freqStack.push (4);//堆栈是 [5,7,5,7,4]
freqStack.push (5);//堆栈是 [5,7,5,7,4,5]
freqStack.pop ();//返回 5 ，因为 5 出现频率最高。堆栈变成 [5,7,5,7,4]。
freqStack.pop ();//返回 7 ，因为 5 和 7 出现频率最高，但7最接近顶部。堆栈变成 [5,7,5,4]。
freqStack.pop ();//返回 5 ，因为 5 出现频率最高。堆栈变成 [5,7,4]。
freqStack.pop ();//返回 4 ，因为 4, 5 和 7 出现频率最高，但 4 是最接近顶部的。堆栈变成 [5,7]。
 

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-frequency-stack
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```java
class FreqStack {

   
        static class Ele {
            int element;
            int index;
        }

        List<Ele> scales;

        PriorityQueue<Integer> maxs;


        public FreqStack() {
            scales = new ArrayList<>();
            maxs = new PriorityQueue<>((a,b) -> b - a);
        }

        public void push(int val) {
            int n = scales.size();
            Ele e = new Ele();
            e.element = val;
            scales.add(e);
            for (int i = n - 1; i >= 0; i--) {
                Ele ele = scales.get(i);
                if (ele.element == val) {
                    int currentMax = ele.index + 1;
                    e.index = currentMax;
                    maxs.add(currentMax);
                    return;
                }
            }
            e.index = 1;
            maxs.add(1);
        }

        public int pop() {
            int n = scales.size();
            int currentMax = maxs.poll();
            for (int i = n - 1; i >= 0; i--) {
                Ele current = scales.get(i);
                if (currentMax == current.index) {
                    return scales.remove(i).element;
                }
            }
            return scales.remove(0).element;
        }

}

/**
 * Your FreqStack object will be instantiated and called as such:
 * FreqStack obj = new FreqStack();
 * obj.push(val);
 * int param_2 = obj.pop();
 */
```
