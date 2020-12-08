## 字母异位词分组
给定一个字符串数组，将字母异位词组合在一起。字母异位词指字母相同，但排列不同的字符串。

示例:

输入: ["eat", "tea", "tan", "ate", "nat", "bat"]
输出:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
]
说明：

所有输入均为小写字母。
不考虑答案输出的顺序。

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvaszc/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


```go
func groupAnagrams(strs []string) [][]string {

    checkList := make(map[string]int)

    returns := make([][]string,len(strs)+1)

    if len(strs) == 0{
        return returns
    }

    var key string
    m := 1
    for i:=0;i< len(strs);i++{
        key = createKey(strs[i])
        if checkList[key] != 0{
            returns[checkList[key]] = append(returns[checkList[key]],strs[i])
        }else{
            checkList[key] = m
            returns[m] = append(returns[m],strs[i])
            m +=1
        }
	}

    return returns[1:m]

}

func  createKey(st string)string{
    list:= make([]int,26);
    
    for _,val:= range st {
        list[val - 'a']++
    }
    
    returns := ""
    for i:=0 ;i < len(list);i++{
        if list[i] == 0{
            continue
        }else{
            returns = strconv.Itoa(i)+strconv.Itoa(list[i])+returns 
        }
    }
    return returns
}
```
