##  数组序号转换

给你一个整数数组 arr ，请你将数组中的每个元素替换为它们排序后的序号。

序号代表了一个元素有多大。序号编号的规则如下：

序号从 1 开始编号。
一个元素越大，那么序号越大。如果两个元素相等，那么它们的序号相同。
每个数字的序号都应该尽可能地小。
 

示例 1：

输入：arr = [40,10,20,30]
输出：[4,1,2,3]
解释：40 是最大的元素。 10 是最小的元素。 20 是第二小的数字。 30 是第三小的数字。
示例 2：

输入：arr = [100,100,100]
输出：[1,1,1]
解释：所有元素有相同的序号。


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/rank-transform-of-an-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func arrayRankTransform(arr []int) []int {
    a := append([]int{}, arr...)
    sort.Ints(a)
    ranks := map[int]int{}
    for _, v := range a {
        if _, ok := ranks[v]; !ok {
            ranks[v] = len(ranks) + 1
        }
    }
    for i, v := range arr {
        arr[i] = ranks[v]
    }
    return arr
}
```
