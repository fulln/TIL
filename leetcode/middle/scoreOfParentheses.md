##  括号的分数

给定一个平衡括号字符串 S，按下述规则计算该字符串的分数：

() 得 1 分。
AB 得 A + B 分，其中 A 和 B 是平衡括号字符串。
(A) 得 2 * A 分，其中 A 是平衡括号字符串。
 

示例 1：

输入： "()"
输出： 1
示例 2：

输入： "(())"
输出： 2
示例 3：

输入： "()()"
输出： 2
示例 4：

输入： "(()(()))"
输出： 6

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/score-of-parentheses
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func scoreOfParentheses(s string) int {
    // 栈入栈出
    sum := 0
    n :=1 
    for i:=1;i < len(s);i++{
        if s[i] == '('{
            if n == 0{
                n = 1    
            }else{
                n <<= 1            
            }            
        }else{
            if s[i-1] == '('{
                sum += n
            }
            n >>=1             
        }
    }    
    return sum
}

``` 

