## 困于环中的机器人
在无限的平面上，机器人最初位于 (0, 0) 处，面朝北方。机器人可以接受下列三条指令之一：

"G"：直走 1 个单位
"L"：左转 90 度
"R"：右转 90 度
机器人按顺序执行指令 instructions，并一直重复它们。

只有在平面中存在环使得机器人永远无法离开时，返回 true。否则，返回 false。

 

示例 1：

输入："GGLLGG"
输出：true
解释：
机器人从 (0,0) 移动到 (0,2)，转 180 度，然后回到 (0,0)。
重复这些指令，机器人将保持在以原点为中心，2 为半径的环中进行移动。
示例 2：

输入："GG"
输出：false
解释：
机器人无限向北移动。
示例 3：

输入："GL"
输出：true
解释：
机器人按 (0, 0) -> (0, 1) -> (-1, 1) -> (-1, 0) -> (0, 0) -> ... 进行移动。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/robot-bounded-in-circle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func isRobotBounded(instructions string) bool {
    // 方向d = 0,1,2,3
    d := [][2]int{[2]int{1, 0}, [2]int{0, -1}, [2]int{-1, 0}, [2]int{0, 1}}

    curPoint := [2]int{0, 0}
    curD := 0
    for t := 0; t < 4; t++ {
        for  i := range instructions {
            if instructions[i] == 'G' {
                curPoint[0] += d[curD][0]
                curPoint[1] += d[curD][1]
            } else if instructions[i] == 'L' {
                curD++
                curD %= 4
            } else {
                curD += 3
                curD %= 4
            }
        }
    }
   
    return curPoint == [2]int{0, 0}


}


```
