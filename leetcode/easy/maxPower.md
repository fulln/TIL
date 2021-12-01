## 连续字符

给你一个字符串 s ，字符串的「能量」定义为：只包含一种字符的最长非空子字符串的长度。

请你返回字符串的能量。

 
 ```go
 func maxPower(s string) (ans int) {
    i:=0
    for j :=range s{
        if s[i] != s[j]{
            if j-i>ans{
                ans=j-i
            }
            i=j
        }
        if j==len(s)-1{
            if j-i+1>ans{
                ans=j-i+1
            }
            return
        }
    }
    return
}

 ```
