## 美式键盘

给你一个字符串数组 words ，只返回可以使用在 美式键盘 同一行的字母打印出来的单词。键盘如下图所示。

美式键盘 中：

第一行由字符 "qwertyuiop" 组成。
第二行由字符 "asdfghjkl" 组成。
第三行由字符 "zxcvbnm" 组成。
American keyboard

 

示例 1：

输入：words = ["Hello","Alaska","Dad","Peace"]
输出：["Alaska","Dad"]
示例 2：

输入：words = ["omk"]
输出：[]
示例 3：

输入：words = ["adsdf","sfd"]
输出：["adsdf","sfd"]
```go
func findWords(words []string) []string {

    str1 := "qwertyuiop";
    str2 := "asdfghjkl";
    ret := []string{}

    for i:=0;i<len(words);i++{
        slen := len(words[i])
        r1,r2 := 0,0

       
        for _,s := range words[i]{
            curr := 0
            for _,key := range str1{
                if key == s {
                    curr = 1
                    r1 ++
                    break
                }
            }
            if curr == 0{
                break
            }
        }

        if r1 != 0 && r1 != slen{
            continue
        }


        for _,s2 := range words[i]{
            curr := 0
            for _,key2 := range str2{
                if key2 == s2 {
                    curr = 1
                    r2 ++
                    break
                }
            }
            if curr == 0{
                break
            }
        }

        
        if r2 != 0 && r2 != slen{
            continue
        }else{
            ret = append(ret,words[i])
        }
    }
    
    return ret


}
```
