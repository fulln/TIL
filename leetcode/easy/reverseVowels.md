## 反转字符串中的元音字母
编写一个函数，以字符串作为输入，反转该字符串中的元音字母。

 

示例 1：

输入："hello"
输出："holle"
示例 2：

输入："leetcode"
输出："leotcede"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reverse-vowels-of-a-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func reverseVowels(s string) string {
    b := []byte(s)
    str := []byte{'a','o','i','e','u','A','O','I','E','U'}
    for from,end:= 0,len(b) -1;from <end ;{
        if include(str,b[from]){
            if  include(str,b[end]){
                b[from],b[end] = b[end],b[from]
                from++
            }
            end --    
        }else{
            from ++
        }
    }
    return string(b)
}

func include(str []byte,s byte)bool{
        for _,val := range str{
            if s == val{
                return true
            }
        }
        return false
}
```
