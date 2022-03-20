## 6030. 由单个字符重复的最长子字符串
给你一个下标从 0 开始的字符串 s 。另给你一个下标从 0 开始、长度为 k 的字符串 queryCharacters ，一个下标从 0 开始、长度也是 k 的整数 下标 数组 queryIndices ，这两个都用来描述 k 个查询。

第 i 个查询会将 s 中位于下标 queryIndices[i] 的字符更新为 queryCharacters[i] 。

返回一个长度为 k 的数组 lengths ，其中 lengths[i] 是在执行第 i 个查询 之后 s 中仅由 单个字符重复 组成的 最长子字符串 的 长度 。

 

示例 1：

输入：s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
输出：[3,3,4]
解释：
- 第 1 次查询更新后 s = "bbbacc" 。由单个字符重复组成的最长子字符串是 "bbb" ，长度为 3 。
- 第 2 次查询更新后 s = "bbbccc" 。由单个字符重复组成的最长子字符串是 "bbb" 或 "ccc"，长度为 3 。
- 第 3 次查询更新后 s = "bbbbcc" 。由单个字符重复组成的最长子字符串是 "bbbb" ，长度为 4 。
因此，返回 [3,3,4] 。
示例 2：

输入：s = "abyzz", queryCharacters = "aa", queryIndices = [2,1]
输出：[2,3]
解释：
- 第 1 次查询更新后 s = "abazz" 。由单个字符重复组成的最长子字符串是 "zz" ，长度为 2 。
- 第 2 次查询更新后 s = "aaazz" 。由单个字符重复组成的最长子字符串是 "aaa" ，长度为 3 。
因此，返回 [2,3] 。
 

提示：

1 <= s.length <= 105
s 由小写英文字母组成
k == queryCharacters.length == queryIndices.length
1 <= k <= 105
queryCharacters 由小写英文字母组成
0 <= queryIndices[i] < s.length
```go
// 暴力解法  超时
func longestRepeating(s string, queryCharacters string, queryIndices []int) []int {
    // 直接统计出来当前最长字串是多少
    ret := []int{}
    max := 0
    for i:=0;i<len(queryIndices);i++{
        max,s= checkEffects(s,queryCharacters[i],queryIndices[i])
        ret = append(ret,max)
    }
    return ret
}


func checkEffects(s string,c byte,i int)(mm int,rs string){
    sc := []byte(s)
    sc[i] = c
    rs = string(sc)
    mm =  getStrMax(rs)
    return
}


func getStrMax(s string)int{
    last,curr,max :=s[0],1,1
    for i:= 1; i< len(s);i++{
        if last ==  s[i]{
            curr ++
            if max < curr{
                max = curr
            }
        }else{
            curr = 1
        }
        last = s[i]
    }
    return max
}

func max(a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}


```
