## 有效的完全平方数
给定一个 正整数 num ，编写一个函数，如果 num 是一个完全平方数，则返回 true ，否则返回 false 。

进阶：不要 使用任何内置的库函数，如  sqrt 。

 

示例 1：

输入：num = 16
输出：true
示例 2：

输入：num = 14
输出：false

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/valid-perfect-square
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func isPerfectSquare(num int) bool {

    if num ==1{
        return true
    }
    start := 1
    end := num /2

    for start <= end {
        middle := start + (end-start) / 2
        res := num / middle
        if middle == res{
            if num % middle == 0{
                return true
            }    
            start = middle +1
        }else if res < middle{
            end = middle -1
        }else{
            start = middle +1
        }
           
    }
    return false

}
```
