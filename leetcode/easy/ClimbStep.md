## 爬楼梯

```go

package main

//假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
//
// 每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
//
// 注意：给定 n 是一个正整数。
//
// 示例 1：
//
// 输入： 2
//输出： 2
//解释： 有两种方法可以爬到楼顶。
//1.  1 阶 + 1 阶
//2.  2 阶
//
// 示例 2：
//
// 输入： 3
//输出： 3
//解释： 有三种方法可以爬到楼顶。
//1.  1 阶 + 1 阶 + 1 阶
//2.  1 阶 + 2 阶
//3.  2 阶 + 1 阶
//
// Related Topics 动态规划
// 👍 1181 👎 0

//1. 分治
//1。走的第一步为1
//2。 1+2 + 1+1
//leetcode submit region begin(Prohibit modification and deletion)
func climbStairs(n int) int {
	return climbStep(1,n)+climbStep(2,n)
}

func climbStep(step int,n int)int{
 //递归容易超时
	if step +1 == n{
		return 1
	}


	if step +2== n{
		return 2
	}

	if climbStep(step,n) == n{
		return 1
	}

}

func climbStairs2(n int) int {
	//后一步的爬法 = 前面2步之和？
	var first, second = 1, 2

	if n == 1 {
		return 1
	}
	if n == 2 {
		return 2
	}
	for i := 3; i <= n; i++ {
		first, second = second, first+second
	}
	return second
}

func main() {
	stairs := climbStairs2(3)
	print(stairs)
}

//leetcode submit region end(Prohibit modification and deletion)
```

