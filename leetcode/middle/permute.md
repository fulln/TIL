## 全排列
给定一个 没有重复 数字的序列，返回其所有可能的全排列。

示例:

输入: [1,2,3]
输出:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]


作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvqup5/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func permute(nums []int) [][]int {
    resp := [][]int{}

    var dfs func([]bool,[]int)
    dfs = func(m []bool,sum []int){

        if len(sum) == len(nums) {
            tmp := make([]int, len(nums))
            copy(tmp, sum)
            resp = append(resp,tmp)
            return
        }

         for i:=0; i<len(nums); i++ {
             if m[i]{
                 continue
             }
            m[i]=true
            sum = append(sum,nums[i])
            dfs(m,sum)
            sum = sum[:len(sum)-1]
            m[i]=false
         }
    }
    var used = make([]bool, len(nums))
    dfs(used,[]int{})

    return resp

}
```
