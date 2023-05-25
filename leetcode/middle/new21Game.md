837. New 21 Game

Medium

1.2K

818

Companies

Alice plays the following game, loosely based on the card game **"21"**.

Alice starts with `0` points and draws numbers while she has less than `k` points. During each draw, she gains an integer number of points randomly from the range `[1, maxPts]`, where `maxPts` is an integer. Each draw is independent and the outcomes have equal probabilities.

Alice stops drawing numbers when she gets `k` **or more points**.

Return the probability that Alice has `n` or fewer points.

Answers within `10-5` of the actual answer are considered accepted.

**Example 1:**

**Input:** n = 10, k = 1, maxPts = 10
**Output:** 1.00000
**Explanation:** Alice gets a single card, then stops.

**Example 2:**

**Input:** n = 6, k = 1, maxPts = 10
**Output:** 0.60000
**Explanation:** Alice gets a single card, then stops.
In 6 out of 10 possibilities, she is at or below 6 points.

**Example 3:**

**Input:** n = 21, k = 17, maxPts = 10
**Output:** 0.73278
```go
func new21Game(n int, k int, maxPts int) float64 {

dp := make([]float64,n+1)

dp[0] = 1

var s float64

if k > 0{

s = float64(1)

}else{

s = float64(0)

}

  

for i:=1;i <=n;i++ {

dp[i] = s / float64(maxPts)

if i < k{

s += dp[i]

}

if i - maxPts >= 0 && i - maxPts < k {

s -= dp[i - maxPts]

}

}

ans := float64(0)

for i:=k;i <=n;i++{

ans += dp[i]

}

  

return ans

}
```