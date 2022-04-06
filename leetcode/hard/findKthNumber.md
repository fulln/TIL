## 440. 字典序的第K小数字
给定整数 n 和 k，返回  [1, n] 中字典序第 k 小的数字。

 

示例 1:

输入: n = 13, k = 2
输出: 10
解释: 字典序的排列是 [1, 10, 11, 12, 13, 2, 3, 4, 5, 6, 7, 8, 9]，所以第二小的数字是 10。
示例 2:

输入: n = 1, k = 1
输出: 1
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/k-th-smallest-in-lexicographical-order
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func findKthNumber(n int, k int) int {
    ans := 1
    for k > 1 {
        num := findDeepCode(ans,ans+1,n)       
        if  k > num{
            k -= num
            ans ++
        }else{
            k --
            ans *= 10
        }
    }
    return ans
}

func findDeepCode(n,n2,l int)int{
    size := 0
    
    for n <= l {
        size += min(l+1,n2) - n
        n *= 10
        n2 *= 10 
    }
    return size
}

func min(a,b int)int{
    if a < b{
        return a
    }else{
        return b
    }
}
```