## 最长快乐字符串
如果字符串中不含有任何 'aaa'，'bbb' 或 'ccc' 这样的字符串作为子串，那么该字符串就是一个「快乐字符串」。

给你三个整数 a，b ，c，请你返回 任意一个 满足下列全部条件的字符串 s：

s 是一个尽可能长的快乐字符串。
s 中 最多 有a 个字母 'a'、b 个字母 'b'、c 个字母 'c' 。
s 中只含有 'a'、'b' 、'c' 三种字母。
如果不存在这样的字符串 s ，请返回一个空字符串 ""。

 

示例 1：

输入：a = 1, b = 1, c = 7
输出："ccaccbcc"
解释："ccbccacc" 也是一种正确答案。
示例 2：

输入：a = 2, b = 2, c = 1
输出："aabbc"
示例 3：

输入：a = 7, b = 1, c = 0
输出："aabaa"
解释：这是该测试用例的唯一正确答案。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-happy-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func longestDiverseString(a int, b int, c int) (ret string) {
	A, B, C, total := 0, 0, 0, a+b+c
	for i := 0; i < total; i++ {
		if (a >= b && a >= c && A != 2) || (B == 2 && a > 0) || (C == 2 && a > 0) {
			ret, a, A, B, C = ret+"a", a-1, A+1, 0, 0
		} else if (b >= a && b >= c && B != 2) || (A == 2 && b > 0) || (C == 2 && b > 0) {
			ret, b, A, B, C = ret+"b", b-1, 0, B+1, 0
		} else if (c >= a && c >= b && C != 2) || (A == 2 && c > 0) || (B == 2 && c > 0) {
			ret, c, A, B, C = ret+"c", c-1, 0, 0, C+1
		}
	}
	return
}

```
