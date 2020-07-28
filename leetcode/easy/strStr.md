## 实现 strStr() 函数。

```go
package main

//实现 strStr() 函数。
//
// 给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如
//果不存在，则返回 -1。
//
// 示例 1:
//
// 输入: haystack = "hello", needle = "ll"
//输出: 2
//
//
// 示例 2:
//
// 输入: haystack = "aaaaa", needle = "bba"
//输出: -1
//
//
// 说明:
//
// 当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。
//
// 对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。
// Related Topics 双指针 字符串
// 👍 502 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func strStr(haystack string, needle string) int {
	if len(needle) == 0 {
		return 0
	}
	if len(haystack) == 0 {
		return -1
	}

	//return  strings.Index(haystack, needle)

	// kmp算法实现
	//kmp()
	return -1
}

func kmp(haystack string, needle string) int {
	//hay := []rune(haystack)
	//need := []rune(needle)
	//lh := len(hay)
	//ln := len(need)

	return 0
}

func get_next(needle []rune) map[int]int {
	var returns = make(map[int]int)

	var length = len(needle)
	begin := 0
	hit := -1
	for begin < length {
		if hit == -1 || needle[hit] == needle[begin] {
			hit++
			begin++
			if needle[begin] != needle[hit] {
				returns[begin] = hit
			} else {
				returns[begin] = returns[hit]
			}
		} else {
			hit = returns[hit]
		}

	}

	return returns
}

func main() {

}

//leetcode submit region end(Prohibit modification and deletion)
```