## copyAndArray 外观数列

```go
//给定一个正整数 n（1 ≤ n ≤ 30），输出外观数列的第 n 项。
//
// 注意：整数序列中的每一项将表示为一个字符串。
//
// 「外观数列」是一个整数序列，从数字 1 开始，序列中的每一项都是对前一项的描述。前五项如下：
//
//1.     1
//2.     11
//3.     21
//4.     1211
//5.     111221
//
//
// 第一项是数字 1
//
// 描述前一项，这个数是 1 即 “一个 1 ”，记作 11
//
// 描述前一项，这个数是 11 即 “两个 1 ” ，记作 21
//
// 描述前一项，这个数是 21 即 “一个 2 一个 1 ” ，记作 1211
//
// 描述前一项，这个数是 1211 即 “一个 1 一个 2 两个 1 ” ，记作 111221
//
//
//
// 示例 1:
//
// 输入: 1
//输出: "1"
//解释：这是一个基本样例。
//
// 示例 2:
//
// 输入: 4
//输出: "1211"
//解释：当 n = 3 时，序列是 "21"，其中我们有 "2" 和 "1" 两组，"2" 可以读作 "12"，也就是出现频次 = 1 而 值 = 2；类似
//"1" 可以读作 "11"。所以答案是 "12" 和 "11" 组合在一起，也就是 "1211"。
// Related Topics 字符串
// 👍 503 👎 0

//leetcode submit region begin(Prohibit modification and deletion)
func countAndSay(n int) string {

	//递归
	var metaCount = []int{1}
	var result string
	for i := 1; i <n; i++ {
		metaCount = recursive(metaCount)
	}

	for i := 0; i < len(metaCount); i++ {
		result = result + strconv.Itoa(metaCount[i])
	}
	return result
}

func recursive(result []int) []int {
	var curr = result[0]
	index := 0
	var array []int
	for i := 0; i < len(result); i++ {
		if curr != result[i] {
			array = append(array, index, curr)
			curr = result[i]
			index = 1
		} else {
			index++
		}
	}
	array = append(array, index, curr)
	return array
}

func main() {
	say := countAndSay(2)
	print(say)
	//var back string
	//var count = []int{1, 2, 34, 5}
	//for e := range count {
	//	back = back + strconv.Itoa(count[e])
	//}
	//print(back)
}

//leetcode submit region end(Prohibit modification and deletion)

```

