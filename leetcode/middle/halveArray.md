## 将数组和减半的最少操作次数

给你一个正整数数组 nums 。每一次操作中，你可以从 nums 中选择 任意 一个数并将它减小到 恰好 一半。（注意，在后续操作中你可以对减半过的数继续执行操作）

请你返回将 nums 数组和 至少 减少一半的 最少 操作数。

 

示例 1：

输入：nums = [5,19,8,1]
输出：3
解释：初始 nums 的和为 5 + 19 + 8 + 1 = 33 。
以下是将数组和减少至少一半的一种方法：
选择数字 19 并减小为 9.5 。
选择数字 9.5 并减小为 4.75 。
选择数字 8 并减小为 4 。
最终数组为 [5, 4.75, 4, 1] ，和为 5 + 4.75 + 4 + 1 = 14.75 。
nums 的和减小了 33 - 14.75 = 18.25 ，减小的部分超过了初始数组和的一半，18.25 >= 33/2 = 16.5 。
我们需要 3 个操作实现题目要求，所以返回 3 。
可以证明，无法通过少于 3 个操作使数组和减少至少一半。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-operations-to-halve-array-sum
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
class Solution {
    public int halveArray(int[] nums) {
        double sum = 0;
        int ans = 0;
        Queue<Double> pq = new PriorityQueue<>((x, y) -> Double.compare(y , x));

        for (int val : nums) {
            sum += val;
            pq.add((double) val);
        }

        double target = sum / 2;

        while (sum > target) {
            double n = pq.poll();
            sum -= n / 2;
            ans++;
            pq.add(n / 2);
        }

        return ans;

        
    }
}
```
