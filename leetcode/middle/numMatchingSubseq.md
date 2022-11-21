##  匹配子序列的单词数

792. 匹配子序列的单词数
给定字符串 s 和字符串数组 words, 返回  words[i] 中是s的子序列的单词个数 。

字符串的 子序列 是从原始字符串中生成的新字符串，可以从中删去一些字符(可以是none)，而不改变其余字符的相对顺序。

例如， “ace” 是 “abcde” 的子序列。
 

示例 1:

输入: s = "abcde", words = ["a","bb","acd","ace"]
输出: 3
解释: 有三个是 s 的子序列的单词: "a", "acd", "ace"。
Example 2:

输入: s = "dsahjpjauf", words = ["ahjpjau","ja","ahbwzgqnuk","tnmlanowax"]
输出: 2
 

提示:

1 <= s.length <= 5 * 104
1 <= words.length <= 5000
1 <= words[i].length <= 50
words[i]和 s 都只由小写字母组成。
​​​​
通过次数25,496提交次数50,870

```go
func numMatchingSubseq(s string, words []string) (ans int) {
    type pair struct{ i, j int }
    ps := [26][]pair{}
    for i, w := range words {
        ps[w[0]-'a'] = append(ps[w[0]-'a'], pair{i, 0})
    }
    for _, c := range s {
        q := ps[c-'a']
        ps[c-'a'] = nil
        for _, p := range q {
            p.j++
            if p.j == len(words[p.i]) {
                ans++
            } else {
                w := words[p.i][p.j] - 'a'
                ps[w] = append(ps[w], p)
            }
        }
    }
    return
}


```

