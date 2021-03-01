## 分割回文串

给定一个字符串 s，将 s 分割成一些子串，使每个子串都是回文串。

返回 s 所有可能的分割方案。

示例:

输入: "aab"
输出:
[
  ["aa","b"],
  ["a","a","b"]
]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions/xaxi62/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func partition(s string) [][]string {
    returns := make([][]string,0)
	cur := make([]string,0)
    recurseP(cur,&returns,0,s)
    return returns
}

func checkP(s string) bool {
	for i,j := 0,len(s)-1; i < j; i,j = i+1,j-1 {
		if s[i] != s[j] {
			return false
		}
	}
	return true
}

func recurseP(cur []string, ret *[][]string, index int, s string) {
	if index == len(s) {
		tmp := make([]string,len(cur))
		copy(tmp,cur)
		*ret = append(*ret,tmp)
		return
	}

	for i:=index; i<len(s); i++ {
		if checkP(s[index:i+1]) {
			cur = append(cur, s[index:i+1])
			recurseP(cur,ret,i+1,s)
			cur = cur[:len(cur)-1]
		}
	}
}

```

