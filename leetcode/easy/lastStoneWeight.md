You are given an array of integers `stones` where `stones[i]` is the weight of the `ith` stone.

We are playing a game with the stones. On each turn, we choose the **heaviest two stones** and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:

-   If `x == y`, both stones are destroyed, and
-   If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return _the weight of the last remaining stone_. If there are no stones left, return `0`.

**Example 1:**

**Input:** stones = [2,7,4,1,8,1]
**Output:** 1
**Explanation:** 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

**Example 2:**

**Input:** stones = [1]
**Output:** 1

**Constraints:**

-   `1 <= stones.length <= 30`
-   `1 <= stones[i] <= 1000`

```go
  

func lastStoneWeight(stones []int) int {

maxHeap := &MaxHeap{}

  

for _, stone := range stones {

heap.Push(maxHeap, stone)

}

  

for maxHeap.Len() > 1 {

stone1 := heap.Pop(maxHeap).(int)

stone2 := heap.Pop(maxHeap).(int)

  

if stone1 != stone2 {

heap.Push(maxHeap, stone1 - stone2)

}

}

  

res := 0

if maxHeap.Len() == 1 {

res = (*maxHeap)[0]

}

return res

}

  
  
  

type MaxHeap []int

  

func (h MaxHeap) Len() int { return len(h) }

func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] }

func (h MaxHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }

  

func (h *MaxHeap) Push(x interface{}) {

*h = append(*h, x.(int))

}

  

func (h *MaxHeap) Pop() interface{} {

x := (*h)[len(*h)-1]

*h = (*h)[:len(*h)-1]

return x

}
```