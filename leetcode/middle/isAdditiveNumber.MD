## 累加数
累加数 是一个字符串，组成它的数字可以形成累加序列。

一个有效的 累加序列 必须 至少 包含 3 个数。除了最开始的两个数以外，字符串中的其他数都等于它之前两个数相加的和。

给你一个只包含数字 '0'-'9' 的字符串，编写一个算法来判断给定输入是否是 累加数 。如果是，返回 true ；否则，返回 false 。

说明：累加序列里的数，除数字 0 之外，不会 以 0 开头，所以不会出现 1, 2, 03 或者 1, 02, 3 的情况。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/additive-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func isAdditiveNumber(num string) bool {
	n := len(num)
	if n < 3 {
		return false
	}
	for i := 1; i < n; i++ {
		if i > 1 && num[0] == '0' { // 排除前导 0
			break
		}
		if lst, _ := strconv.Atoi(num[:i]); dfs(num, lst, i) {  // 不是很优雅的递归
			return true
		}
	}
	return false
}

func dfs(num string, lst int, idx int) bool {
	n := len(num)
	isAdditive := false
	for nxtStart := idx + 1; nxtStart < n; nxtStart++ {
		if nxtStart > idx+1 && num[idx] == '0' {   // 排除前导 0
			break
		}
		cur, _ := strconv.Atoi(num[idx:nxtStart])   // 第二个数
		sum := strconv.Itoa(cur + lst)              // 第一个数和第二个数的和
		dur := len(sum)                             // 第三个数的长度
		nxtEnd := nxtStart + dur                    // 第三个数的右区间
		if nxtEnd > n {                             // 如果右区间越界，结束循环
			break
		}
		if sum == num[nxtStart:nxtEnd] {            // 如果和相等
			if nxtEnd == n {                        // 并且刚好到数组的最后一位，则为累加数
				return true
			}
			isAdditive = dfs(num, cur, nxtStart)     // 没到结尾就继续递归
		}
	}
	return isAdditive
}
```
