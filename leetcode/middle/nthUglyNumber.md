## 剑指 Offer 49. 丑数

我们把只包含质因子 2、3 和 5 的数称作丑数（Ugly Number）。求按从小到大的顺序的第 n 个丑数。

 

示例:

输入: n = 10
输出: 12
解释: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 是前 10 个丑数。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/chou-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
[200~func nthUglyNumber(n int) int {
	if n <= 0{
        return 0
    
	}
    dp := make([]int,n)
    dp[0] = 1
    m,s,k := 0,0,0
    for i:=1;i< n;i++{
        dp[i] =min(min(dp[m]*2,dp[s]*3),dp[k]*5)
		if dp[i] == dp[m]*2{
            m++
        
		}
	if dp[i]  == dp[s]*3{
            s++
        
	}
	if dp[i] == dp[k]*5{
            k++
        
	}
    
    }
    return dp[n-1]

}

func min(a,b int)int{
	if a > b{
        return b
    
	}else{
        return a
    
	}

}]

```
