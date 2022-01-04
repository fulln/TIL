## 按位与为零的三元组
给定一个整数数组 A，找出索引为 (i, j, k) 的三元组，使得：

0 <= i < A.length
0 <= j < A.length
0 <= k < A.length
A[i] & A[j] & A[k] == 0，其中 & 表示按位与（AND）操作符。
 

示例：

输入：[2,1,3]
输出：12
解释：我们可以选出如下 i, j, k 三元组：
(i=0, j=0, k=1) : 2 & 2 & 1
(i=0, j=1, k=0) : 2 & 1 & 2
(i=0, j=1, k=1) : 2 & 1 & 1
(i=0, j=1, k=2) : 2 & 1 & 3
(i=0, j=2, k=1) : 2 & 3 & 1
(i=1, j=0, k=0) : 1 & 2 & 2
(i=1, j=0, k=1) : 1 & 2 & 1
(i=1, j=0, k=2) : 1 & 2 & 3
(i=1, j=1, k=0) : 1 & 1 & 2
(i=1, j=2, k=0) : 1 & 3 & 2
(i=2, j=0, k=1) : 3 & 2 & 1
(i=2, j=1, k=0) : 3 & 1 & 2

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/triples-with-bitwise-and-equal-to-zero
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func countTriplets(nums []int) int {
    cnt := make([]int,1 << 16)
    for _,i := range nums{
        for _,j := range nums{
            cnt[ i&j ] ++
        }    
    }
    sum := 0

    for _,k := range nums{
        m :=  k^(len(cnt) -1)
        for i:=m;i != 0;i = m & (i-1){
            sum += cnt[i]
        } 
        sum +=cnt[0]
    }


    return sum

}
```
