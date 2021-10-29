## 路径交叉
给你一个整数数组 distance 。

从 X-Y 平面上的点 (0,0) 开始，先向北移动 distance[0] 米，然后向西移动 distance[1] 米，向南移动 distance[2] 米，向东移动 distance[3] 米，持续移动。也就是说，每次移动后你的方位会发生逆时针变化。

判断你所经过的路径是否相交。如果相交，返回 true ；否则，返回 false 。

 

示例 1：


输入：distance = [2,1,1,2]
输出：true
示例 2：


输入：distance = [1,2,3,4]
输出：false
示例 3：


输入：distance = [1,1,1,1]
输出：true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/self-crossing
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func isSelfCrossing(distance []int) bool {
    for i := 3; i < len(distance); i++ {
        // 第 1 类路径交叉的情况
        if distance[i] >= distance[i-2] && distance[i-1] <= distance[i-3] {
            return true
        }

        // 第 2 类路径交叉的情况
        if i == 4 && distance[3] == distance[1] &&
            distance[4] >= distance[2]-distance[0] {
            return true
        }

        // 第 3 类路径交叉的情况
        if i >= 5 && distance[i-3]-distance[i-5] <= distance[i-1] &&
            distance[i-1] <= distance[i-3] &&
            distance[i] >= distance[i-2]-distance[i-4] &&
            distance[i-2] > distance[i-4] {
            return true
        }
    }
    return false
}
```
