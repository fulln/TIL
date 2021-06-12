## 动态规划

动态规划(dynamic programming)是运筹学的一个分支，是求解决策过程(decision process)最优化的数学方法

动态规划在算法中,算的上是最考验思路的一种类型的题,也是我认为最能称之为算法的题型,要求得到状态转移方程,然后以状态转移方程去倒推具体的解.从而达到某一特定解恰好能满足题目.

## 状态转移方程

这里，引出「状态转移方程」这个名词，实际上就是描述问题结构的数学形式：

可见列出「状态转移方程」的重要性，它是解决问题的核心。

很容易发现，其实状态转移方程直接代表着暴力解法。

千万不要看不起暴力破解，动态规划问题最困难的就是写出状态转移方程，

 ### 经典题型思路

 - 01背包问题

   > 动态规划问题背包9问,学习还是要看大佬视频  [AcWing 2. 01背包问题 - AcWing](https://www.acwing.com/video/214/)

    有 N 件物品和一个容量是 V 的背包。每件物品只能使用一次。第 i件物品的体积是 vi，价值是 wi。求解将哪些物品装入背包，可使这些物品的总体积不超过背包容量，且总价值最大。输出最大价值。 

   ```go
   /**
    该问题属于01背包问题
    
    首先看2维怎么推到通用解
    
    如果最大价值是存在前i个物品的总体积j里面中的一个
    
    那么第i件物品有没有加入必要,有下面2个判断
    
    1. 如果不用的物品
    	f[i][j] = f[i -1][j]
    2. 如果需要i个物品,则剩下的最多能装 j -v[i]个体积,此时最大值是: 
    	f[i][j] = f[i-1][j - v[i]]+w[i]
   
   然后默认f[i][0]都是从0开始递增
    	
   最终答案在这2种情况中的最大值
    */
   func package(v,w []int){
       f := make([][]int,len(v))
       
       for _,val := range f{
           val := make([]int,n+1)
       }
       
       for i := 1; i <= len(v); i++ {
           for j := 0; j <= len(w); j++ {
               f[i][j] =f[i -1][j]
               if j >= v[i]{
                   f[i][j] = max(f[i-1][j],f[i-1][j-v[i]]+w[i])
               }
           }
       }
       return f[len(v) -1][len(w) -1]
   }
   
   func max(a,b int)int{
       if a > b {
           return a
       }else{
           return b
       }
   }
   ```

   ### 滚动数组

   滚动数组是DP中的一种编程思想。

   简单的理解就是让数组滚动起来，每次都使用固定的几个存储空间，来达到压缩，节省存储空间的作用。

   因为 DP 题目是一个自底向上的扩展过程，**我们常常需要用到的是连续的解，前面的解往往可以舍去**，所以用滚动数组优化是很有效的。

   

   ```xml
   假设一个状态方程为 dp[i][j] = dp[i-1][j-1] + 1;
   
   1. 从前往后去设置值
     dp[i-1][j-1]的值的结果就是我们这次循环得到的值
   2. 从后往前去设置值
     dp[i-1][j-1]的值的结果就是我们上一次循环得到的值
   
   根据滚动数组的思想,我们在状态转移的过程中, 是需要上一轮得到的结果来得到我们现在这一轮的值的结果,这样在每次循环的时候, 上一轮的结果不会被覆盖重新计算
    
   ```

   

   

- 01背包问题一维优化

  ```go
  /**
    其实通过上面的推导的公式, 不难得到,它的f[i] 只与f[i-1]相关联,
    f[i]就表示在体积在i的情况下,它的最大价值是多少. 
    f[i] 在初始化时为0
    
    总体积k < m 时,f[k] 为 价值最大值
    
    有以下推导公式
    
    f[m - k] = f[m - k +v[0]] + w[0] 
    	
    
   */
  func package(v,w []int){
      f := make([]int,len(v))
      
      for i := 1; i <= len(v); i++ {
          for j := len(w) -1 ; j >= v(i); j-- {
              if j >= v[i]{
                  f[j] = max(f[j],f[j-v[i]]+w[i])
              }
          }
      }
      return f[len(w) -1]
  }
  
  ```

- 最后一块石头的重量

   有一堆石头，用整数数组 stones 表示。其中 stones[i] 表示第 i 块石头的重量。

  每一回合，从中选出任意两块石头，然后将它们一起粉碎。假设石头的重量分别为 x 和 y，且 x <= y。那么粉碎的可能结果如下：

  如果 x == y，那么两块石头都会被完全粉碎； 如果 x != y，那么重量为 x 的石头将会完全粉碎，而重量为 y 的石头新重量为 y-x。 最后，最多只会剩下一块 石头。返回此石头 最小的可能重量 。如果没有石头剩下，就返回 0。

  ```go
  /**
  
    这个问题就是就是求2堆之差最小问题,那么按照上面的题目思路,其状态转移方程为
  		 f[i] = f[i-stones[0]] + stone[0]
    然后需要自底而上的倒推,以免重复计算
    
   */
  func lastStoneWeightII(stones []int) int {
      //无脑动态规划 一转背包问题
      
      if len(stones) == 0{
          return 0
      }
      sum :=0
      for _,val:= range stones{
          sum +=val
      }
  
      dp := make([]int,sum / 2 + 1)
      
      for i:= 0;i< len(stones);i++{
          for j:= sum / 2 ;j >= stones[i];j--{
              dp[j]  = max(dp[j],dp[j - stones[i]]+stones[i]) 
          }
      }
      return sum -dp[sum/2]*2
      
  }
  func max(a,b int)int{
      if a > b {
          return a
      }else
      {
          return b
      }
  }
  ```

- 一和零

  给你一个二进制字符串数组 strs 和两个整数 m 和 n 。

  请你找出并返回 strs 的最大子集的大小，该子集中 最多 有 m 个 0 和 n 个 1 。

  如果 x 的所有元素也是 y 的元素，集合 x 是集合 y 的 子集 。

  ```go
  func findMaxForm(strs []string, m int, n int) int {
      if len(strs) == 0{
          return 0
      }
  
      dp := make([][]int,m+1)
  
      for z:=0;z<m+1;z++{
          dp[z] = make([]int,n+1)
      }
  
      for _,val := range strs{
          one := 0
          zero := 0
          for _,val := range val{
              if '0' == val{
                  zero ++
              }else{
                  one ++
              }
          }
  
          for i :=m;i >= zero;i--{
              for j:= n;j>=one;j--{
                  dp[i][j] = Max(dp[i][j],1+ dp[i-zero][j-one])
              }
          } 
      }
  
      return dp[m][n]
  
  }
  
  func Max(a ,b int) int{
          if a > b{
              return a
          }
          return b
      }
  ```

  

### 参考

 [动态规划空间优化之滚动数组](https://blog.csdn.net/qq_36378681/article/details/98657014)
