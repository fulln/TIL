## 完美数
对于一个 正整数，如果它和除了它自身以外的所有 正因子 之和相等，我们称它为 「完美数」。

给定一个 整数 n， 如果是完美数，返回 true，否则返回 false

 

示例 1：

输入：num = 28
输出：true
解释：28 = 1 + 2 + 4 + 7 + 14
1, 2, 4, 7, 和 14 是 28 的所有正因子。
示例 2：

输入：num = 6
输出：true
示例 3：

输入：num = 496
输出：true
示例 4：

输入：num = 8128
输出：true
示例 5：

输入：num = 2
输出：false

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/perfect-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func checkPerfectNumber(num int) bool {
    if num ==1{
        return false
    }
    sum := 1
    for i:=2 ;sum <= num && i*i <= num;i++{
        if  num%i == 0{
            sum += i 
            if i*i < num {
                sum += num / i
            }
        }
    }
    return  num >0 && sum == num
}
```
