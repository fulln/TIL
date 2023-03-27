
## 1638. 统计只差一个字符的子串数目

给你两个字符串 s 和 t ，请你找出 s 中的非空子串的数目，这些子串满足替换 一个不同字符 以后，是 t 串的子串。换言之，请你找到 s 和 t 串中 恰好 只有一个字符不同的子字符串对的数目。

比方说， "computer" and "computation" 只有一个字符不同： 'e'/'a' ，所以这一对子字符串会给答案加 1 。

请你返回满足上述条件的不同子字符串对数目。

一个 子字符串 是一个字符串中连续的字符。

 

示例 1：

输入：s = "aba", t = "baba"
输出：6
解释：以下为只相差 1 个字符的 s 和 t 串的子字符串对：
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
("aba", "baba")
加粗部分分别表示 s 和 t 串选出来的子字符串。
示例 2：
输入：s = "ab", t = "bb"
输出：3
解释：以下为只相差 1 个字符的 s 和 t 串的子字符串对：
("ab", "bb")
("ab", "bb")
("ab", "bb")
加粗部分分别表示 s 和 t 串选出来的子字符串。
示例 3：
输入：s = "a", t = "a"
输出：0
示例 4：

输入：s = "abe", t = "bbc"
输出：10

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/count-substrings-that-differ-by-one-character
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func countSubstrings(s string, t string) int {

  

    ls := len(s)

    lt := len(t)

  

    ds := make([][]int, ls+1)

    dt := make([][]int, ls+1)

  

    for i:=0;i< ls+1;i++ {

        ds[i] = make([]int,lt+1)

    }

  

    for i:=0;i< ls+1;i++{

        dt[i] = make([]int,lt+1)

    }

  

    for  i := 0; i < ls; i++ {

        for j := 0; j < lt; j++ {

            if s[i] == t[j] {

                ds[i + 1][j + 1] = ds[i][j]+1

            }else{

                ds[i + 1][j + 1] = 0

            }

        }

    }

  
  

    for  i := ls-1; i >= 0 ; i-- {

        for j := lt-1; j >=0 ; j-- {

            if s[i] == t[j] {

                dt[i][j] = dt[i+1][j+1]+1

            }else{

                dt[i][j] = 0

            }

        }

    }

    ans := 0;

    for i:= 0; i < ls; i++ {

        for j:= 0; j < lt; j++ {

            if s[i] != t[j] {

                ans += (ds[i][j] + 1) * (dt[i + 1][j + 1] + 1);

            }

        }

    }

    return ans;

}

```