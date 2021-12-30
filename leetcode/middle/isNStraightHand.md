## 一手顺子

Alice 手中有一把牌，她想要重新排列这些牌，分成若干组，使每一组的牌数都是 groupSize ，并且由 groupSize 张连续的牌组成。

给你一个整数数组 hand 其中 hand[i] 是写在第 i 张牌，和一个整数 groupSize 。如果她可能重新排列这些牌，返回 true ；否则，返回 false 。

 

示例 1：

输入：hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
输出：true
解释：Alice 手中的牌可以被重新排列为 [1,2,3]，[2,3,4]，[6,7,8]。
示例 2：

输入：hand = [1,2,3,4,5], groupSize = 4
输出：false
解释：Alice 手中的牌无法被重新排列成几个大小为 4 的组。
 

提示：

1 <= hand.length <= 104
0 <= hand[i] <= 109
1 <= groupSize <= hand.length
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/hand-of-straights
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func isNStraightHand(hand []int, groupSize int) bool {
    if len(hand)%groupSize > 0 {
        return false
    }
    sort.Ints(hand)

    s := len(hand) /groupSize

    checks:=make([][]int,s)
    for i,_ := range(checks){
        checks[i] = []int{}
    }

    for i:=0;i< len(hand);i++{
        for j,_ := range checks{
            if len(checks[j]) == groupSize {
                continue
            }

            if len(checks[j]) == 0{
                checks[j] = append(checks[j],hand[i])
                break
            }

            if checks[j][len(checks[j])-1]  ==  hand[i]{
                continue
            }else if checks[j][len(checks[j])-1] ==  hand[i]-1{
                checks[j] = append(checks[j],hand[i])
                break
            }else{
                return false
            }
        }
    }

    fmt.Println(checks)

    return len(checks[s-1]) == groupSize
}

```
