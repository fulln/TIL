## 查找共用字符
给你一个字符串数组 words ，请你找出所有在 words 的每个字符串中都出现的共用字符（ 包括重复字符），并以数组形式返回。你可以按 任意顺序 返回答案。
 

示例 1：

输入：words = ["bella","label","roller"]
输出：["e","l","l"]
示例 2：

输入：words = ["cool","lock","cook"]
输出：["c","o"]
 

提示：

1 <= words.length <= 100
1 <= words[i].length <= 100
words[i] 由小写英文字母组成

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-common-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func commonChars(A []string) []string {
	char_map := make(map[int32]int)
	for _,ch := range A[0] {
		char_map[ch] = strings.Count(A[0], string(ch))
	}
	for i:=1;i<len(A);i++{
		for _,ch := range A[0] {
			n:=strings.Count(A[i], string(ch))
			if char_map[ch]>n{
				char_map[ch]=n
			}
		}
	}
	result := []string{}
	for ch,n := range char_map{
		for i:=0;i<n;i++{
			result=append(result, string(ch))
		}
	}
	return result
}
```
