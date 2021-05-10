## 丑数

给你一个整数 n ，请你判断 n 是否为 丑数 。如果是，返回 true ；否则，返回 false 。

丑数 就是只包含质因数 2、3 和/或 5 的正整数。

 

示例 1：

输入：n = 6
输出：true
解释：6 = 2 × 3
示例 2：

输入：n = 8
输出：true
解释：8 = 2 × 2 × 2
示例 3：

输入：n = 14
输出：false
解释：14 不是丑数，因为它包含了另外一个质因数 7 。
示例 4：

输入：n = 1
输出：true
解释：1 通常被视为丑数。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ugly-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func isUgly(n int) bool {

    nums :=[]int{2,3,5}

    if n == 0 {
        return false
    }

    if n ==1{
        return true
    }

    for _,val := range nums{
        mod := n % val
        rest := n / val

        if mod != 0 {
            continue
        }

        if contains(rest,nums){
            return true
        }

        if isUgly(rest){
            return true
        }
    }
    return false
}

func contains(n int,nums []int)bool{
    for _,val := range nums{
        if n == val{
            return true
        }
    }
    return false
}
```
