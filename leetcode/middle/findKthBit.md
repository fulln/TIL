## 出第 N 个二进制字符串中的第 K 位

给你两个正整数 n 和 k，二进制字符串  Sn 的形成规则如下：

S1 = "0"
当 i > 1 时，Si = Si-1 + "1" + reverse(invert(Si-1))
其中 + 表示串联操作，reverse(x) 返回反转 x 后得到的字符串，而 invert(x) 则会翻转 x 中的每一位（0 变为 1，而 1 变为 0）。

例如，符合上述描述的序列的前 4 个字符串依次是：

S1 = "0"
S2 = "011"
S3 = "0111001"
S4 = "011100110110001"
请你返回  Sn 的 第 k 位字符 ，题目数据保证 k 一定在 Sn 长度范围以内。

 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-kth-bit-in-nth-binary-string
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func inverse(ch byte) byte {
    if ch == '0' {
        return '1'
    } else {
        return '0'
    }
}

func findKthBit(n int, k int) byte {
    if n == 1 {
        return '0'
    }
    total := 1 << n - 1
    mid := (total + 1) / 2
    if k == mid {
        return '1'
    } else if k < mid {
        return findKthBit(n - 1, k)
    } else {
        b := findKthBit(n - 1, mid - (k - mid))
        return inverse(b)
    }
}

```
