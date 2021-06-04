## 比较字符串最小字母出现频次

定义一个函数 f(s)，统计 s  中（按字典序比较）最小字母的出现频次 ，其中 s 是一个非空字符串。

例如，若 s = "dcce"，那么 f(s) = 2，因为字典序最小字母是 "c"，它出现了 2 次。

现在，给你两个字符串数组待查表 queries 和词汇表 words 。对于每次查询 queries[i] ，需统计 words 中满足 f(queries[i]) < f(W) 的 词的数目 ，W 表示词汇表 words 中的每个词。

请你返回一个整数数组 answer 作为答案，其中每个 answer[i] 是第 i 次查询的结果。

 

示例 1：

输入：queries = ["cbd"], words = ["zaaaz"]
输出：[1]
解释：查询 f("cbd") = 1，而 f("zaaaz") = 3 所以 f("cbd") < f("zaaaz")。
示例 2：

输入：queries = ["bbb","cc"], words = ["a","aa","aaa","aaaa"]
输出：[1,2]
解释：第一个查询 f("bbb") < f("aaaa")，第二个查询 f("aaa") 和 f("aaaa") 都 > f("cc")。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/compare-strings-by-frequency-of-the-smallest-character
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func numSmallerByFrequency(queries []string, words []string) []int {

    ret :=[]int{}
    curr :=make([]int,12)
    for _,val := range words{
        curr[find(val)]++
    }

    for i:=len(curr)-1; i > 0 ;i-- {
        curr[i-1] = curr[i] +curr[i-1]
    }

    for  _,val := range queries{
           now :=find(val)
           ret = append(ret,curr[now+1])
    }    

    return ret


}

func find( c string)int{
    small := 0
    smaller := 'z'
    for _,value := range c{
        if smaller > value{
            small  = 1
            smaller = value
        }else if smaller == value{
            small ++
        }
    }
    return small
}




```
