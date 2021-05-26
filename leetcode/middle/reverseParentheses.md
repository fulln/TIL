## 反转每对括号间的子串

给出一个字符串 s（仅含有小写英文字母和括号）。

请你按照从括号内到外的顺序，逐层反转每对匹配括号中的字符串，并返回最终的结果。

注意，您的结果中 不应 包含任何括号。

 

示例 1：

输入：s = "(abcd)"
输出："dcba"
示例 2：

输入：s = "(u(love)i)"
输出："iloveu"
示例 3：

输入：s = "(ed(et(oc))el)"
输出："leetcode"
示例 4：

输入：s = "a(bcdefghijkl(mno)p)q"
输出："apmnolkjihgfedcbq"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-substrings-between-each-pair-of-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func reverseParentheses(s string) string {
    // 字符串无法直接修改，转换为byte slice
    brr := []byte(s)
    var stack []int
    for i := 0; i < len(brr); i ++ {
        if brr[i] == '(' {
            // 遇到左括号，加入栈中
            stack = append(stack, i)
        } else if brr[i] == ')'{
            // 题目保证括号左右匹配，所以不用检验stack中是否有左括号
            lastIdx := stack[len(stack)-1]
            // 反转左括号位置+1到右括号位置-1之间的字符
            for lj, rj := lastIdx + 1, i - 1; lj < rj; lj, rj = lj +1, rj -1 {
                brr[lj], brr[rj] = brr[rj], brr[lj]
            }
            // 已匹配的左括号退栈
            stack = stack[:len(stack)-1]
        }
    }

    // 去掉所有括号字符
    sb := strings.Builder{}
    for i := 0; i < len(brr); i ++ {
        if brr[i] != '(' && brr[i] !=')' {
            sb.WriteByte(brr[i])
        }
    }

    return sb.String()
}

```
