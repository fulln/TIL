## 最长回文子串

给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。

示例 1：

输入: "babad"
输出: "bab"
注意: "aba" 也是一个有效答案。
示例 2：

输入: "cbbd"
输出: "bb"

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvn3ke/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go

func longestPalindrome(s string) string {
    //中心扩散法
    left,right,lens,max,maxLen,maxStart := 0,0,1,0,0,0

    for i := 0;i< len(s);i++{
        left = i-1;
        right = i+1

        for left >=0 && s[i] == s[left]{
            left --
            lens +=1
        }

        for right < len(s) && s[i] == s[right]{
            right++
            lens +=1
        }

        for  left >=0  && right < len(s) && s[left] == s[right]{
            lens +=2
            left --
            right ++
        }

        if (lens > max) {
                maxLen = lens;
                maxStart = left;
                max = lens
        }
        lens = 1;
    }

    
    return s[maxStart+1:maxStart+maxLen+1]
}

```
