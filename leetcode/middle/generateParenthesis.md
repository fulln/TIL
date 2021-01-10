## 括号生成

数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

 

示例：

输入：n = 3
输出：[
       "((()))",
       "(()())",
       "(())()",
       "()(())",
       "()()()"
     ]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xv33m7/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func generateParenthesis(n int) []string {
    
    resp := []string{}
    var dfs func(int,int,string)

    dfs = func(l ,r int,str string){
        if len(str) == 2*n{
            resp = append(resp,str)
        }

        if l > 0{
            dfs(l-1,r,str+"(")
        }

        if l < r{
            dfs(l,r-1,str+")")
        }
    }

    dfs(n,n,"")

    return resp
}

```
