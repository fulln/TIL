## 1017. 负二进制转换

给你一个整数 n ，以二进制字符串的形式返回该整数的 负二进制（base -2）表示。

注意，除非字符串就是 "0"，否则返回的字符串中不能含有前导零。

 

示例 1：

输入：n = 2
输出："110"
解释：(-2)2 + (-2)1 = 2
示例 2：

输入：n = 3
输出："111"
解释：(-2)2 + (-2)1 + (-2)0 = 3
示例 3：

输入：n = 4
输出："100"
解释：(-2)2 = 4

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/convert-to-base-2
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func baseNeg2(n int) string {

    if n == 0 {

        return "0"

    }

    ans := []byte{}

    k := 1

    for n != 0 {

        if n%2 != 0 {

            ans = append(ans, '1')

            n -= k

        } else {

            ans = append(ans, '0')

        }

        k *= -1

        n /= 2

    }

    for i, j := 0, len(ans)-1; i < j; i, j = i+1, j-1 {

        ans[i], ans[j] = ans[j], ans[i]

    }

    return string(ans)

}
```
