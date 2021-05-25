## 字典序排数
给定一个整数 n, 返回从 1 到 n 的字典顺序。

例如，

给定 n =1 3，返回 [1,10,11,12,13,2,3,4,5,6,7,8,9] 。

请尽可能的优化算法的时间复杂度和空间复杂度。 输入的数据 n 小于等于 5,000,000。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lexicographical-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func lexicalOrder(n int) []int {

    var ret []int
    var dfs func(c int)
    dfs = func(c int) {
        if c > n {
            return
        }else{
            ret = append(ret,c)
            for j:=0;j<10;j++{
                dfs(c * 10 + j)
            }
        }
    } 

    for i:=1;i<10;i++{
        dfs(i)
    }

    return ret

}



```
