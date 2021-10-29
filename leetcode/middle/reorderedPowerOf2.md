## 重新排序得到 2 的幂
给定正整数 N ，我们按任何顺序（包括原始顺序）将数字重新排序，注意其前导数字不能为零。

如果我们可以通过上述方式得到 2 的幂，返回 true；否则，返回 false。

 

示例 1：

输入：1
输出：true
示例 2：

输入：10
输出：false
示例 3：

输入：16
输出：true
示例 4：

输入：24
输出：false
示例 5：

输入：46
输出：true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reordered-power-of-2
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func reorderedPowerOf2(n int) bool {
    //DFS + 剪支
    num := []byte(strconv.Itoa(n))   
    sort.Slice(num,func(i,j int)bool{return num[i] < num[j]   } )
    exists := make([]bool,len(num)) 
    var dfs func(cindex,curr int)bool
    
    dfs = func(cindex,curr int)bool{
        if cindex == len(num){
            return check2(curr)
        }
        for i,val := range num{
            // 首位不能为0  || 字符串已经存在 || 之前的字符串已经有过判断
            if (val == '0' && curr == 0 ) || exists[i] || ( i >0 && !exists[i-1] && val == num[i-1]){
                continue
            }
            exists[i] = true
            if dfs(cindex+1,curr* 10 + int(val- '0')){
                return true
            }
            exists[i] = false
        }
        return false
    } 
    return dfs(0,0)
}

func check2(n int)bool{
    return n&(n-1) == 0 
}
```

