## . 玩筹码

有 n 个筹码。第 i 个筹码的位置是 position[i] 。

我们需要把所有筹码移到同一个位置。在一步中，我们可以将第 i 个筹码的位置从 position[i] 改变为:

position[i] + 2 或 position[i] - 2 ，此时 cost = 0
position[i] + 1 或 position[i] - 1 ，此时 cost = 1
返回将所有筹码移动到同一位置上所需要的 最小代价 。

 

示例 1：



输入：position = [1,2,3]
输出：1
解释：第一步:将位置3的筹码移动到位置1，成本为0。
第二步:将位置2的筹码移动到位置1，成本= 1。
总成本是1。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/minimum-cost-to-move-chips-to-the-same-position
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func minCostToMoveChips(position []int) int {
    // 算奇数位个数 和 偶数位个数的最大值

    left :=0;
    right := 0 
    for i:= 0;i< len(position);i++{
        if position[i] & 1 == 0{
            left ++
        }else{
            right ++
        }
    }
    if left > right{
        return right
    }else{
        return left
    }
}
```
