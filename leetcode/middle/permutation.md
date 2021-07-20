## 输出stirng的所有排序


输入一个字符串，打印出该字符串中字符的所有排列。

 

你可以以任意顺序返回这个字符串数组，但里面不能有重复元素。

 

示例:

输入：s = "abc"
输出：["abc","acb","bac","bca","cab","cba"]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zi-fu-chuan-de-pai-lie-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func permutation(s string) []string {

    ans := make([]string, 0)
	cache := map[string]bool{}
	visited := map[int]bool{}
	
	n := len(s)
	var dfs func(str string)
	dfs = func(str string) {
		if n == len(str) {
			if cache[str] == false {
				ans = append(ans, str)
				cache[str] = true
			}
			return
		}
		for i := 0; i < n; i++ {
			if visited[i] {
				continue
			}
			visited[i] = true
			dfs(str + string(s[i]))
			visited[i] = false
		}
	}
	dfs("")
	return ans

}
```
