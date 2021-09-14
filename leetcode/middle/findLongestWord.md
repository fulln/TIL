## 通过删除字母匹配字典最长字符

给你一个字符串 s 和一个字符串数组 dictionary 作为字典，找出并返回字典中最长的字符串，该字符串可以通过删除 s 中的某些字符得到。

如果答案不止一个，返回长度最长且字典序最小的字符串。如果答案不存在，则返回空字符串。

 

示例 1：

输入：s = "abpcplea", dictionary = ["ale","apple","monkey","plea"]
输出："apple"
示例 2：

输入：s = "abpcplea", dictionary = ["a","b","c"]
输出："a"
```go

func (s string, dictionary []string) string {
    i,j,sum:= 0,0,""
    for _,val :=range dictionary{ 
        i =0
        j =0
        for i < len(val) && j < len(s){
            if val[i]== s[j]{
                if i == len(val) -1{
                    sum =max(val,sum) 
                    break
                }
                i++
                j++
            }else{
                j++
            }
        } 
    }    
    return sum
}

func max(a,b string)string{
    if len(a) > len(b){
        return a
    }else if len(a) == len(b) && a < b{
        return a
    }else{
        return b
    }
}

```