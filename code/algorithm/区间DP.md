---
dg-publish: true
tags:
  - 动态规划
  - 算法
createTime: <% tp.file.creation_date() %>
---
## 区间DP的解题策略

区间 DP 是动态规划的一种常见形式，用于解决区间上的问题。一般来说，区间 DP 问题可以转化为字符串 DP 问题，而字符串 DP 问题的解法是比较常见和成熟的。

区间 DP 的解题策略一般有以下几步：

1. 定义状态：设 $dp_{i,j}$ 表示区间 $[i,j]$ 的某个性质，一般情况下会定义一个二维数组来表示。

2. 定义状态转移方程：根据区间 DP 的特点，状态转移方程通常会涉及到区间的划分。一般来说，区间 DP 的状态转移方程可以分为两种情况：

3. 区间 $[i,j]$ 可以划分为 $[i,k]$ 和 $[k+1,j]$ 两个子区间，此时状态转移方程为 $dp_{i,j}=\text{func}(dp_{i,k},dp_{k+1,j})$。

4. 区间 $[i,j]$ 可以划分为 $[i+1,j]$ 和 $[i,j-1]$ 两个子区间，此时状态转移方程为 $dp_{i,j}=\text{func}(dp_{i+1,j},dp_{i,j-1})$。

5. 处理边界情况：通常情况下，区间 DP 的边界情况是 $dp_{i,i}$，即只有一个元素的情况。需要在状态转移方程中特判。

6. 计算顺序：区间 DP 的计算顺序一般是从小区间到大区间，即先计算长度为 $2$ 的区间，再计算长度为 $3$ 的区间，依次递推到整个区间。

7. 输出结果：根据题目要求输出结果。

以上就是区间 DP 的解题策略，需要注意的是，区间 DP 的状态转移方程和字符串 DP 的状态转移方程有很多相似之处，因此对字符串 DP 的掌握也是解决区间 DP 问题的关键。

## 例题

1.  最长上升子序列（Longest Increasing Subsequence）：[https://leetcode-cn.com/problems/longest-increasing-subsequence/](https://leetcode-cn.com/problems/longest-increasing-subsequence/)	
2.  最大子序和（Maximum Subarray）：[https://leetcode-cn.com/problems/maximum-subarray/](https://leetcode-cn.com/problems/maximum-subarray/)
3.  最长公共子序列（Longest Common Subsequence）：[https://leetcode-cn.com/problems/longest-common-subsequence/](https://leetcode-cn.com/problems/longest-common-subsequence/)
4.  最长回文子串（Longest Palindromic Substring）：[https://leetcode-cn.com/problems/longest-palindromic-substring/](https://leetcode-cn.com/problems/longest-palindromic-substring/)
5.  最大矩形（Maximal Rectangle）：[https://leetcode-cn.com/problems/maximal-rectangle/](https://leetcode-cn.com/problems/maximal-rectangle/)
6. [[minScoreTriangulation#多边形三角剖分的最低得分]]
