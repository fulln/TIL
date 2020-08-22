## 买卖股票的最佳时机
```go

/*
给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。

如果你最多只允许完成一笔交易（即买入和卖出一支股票一次），设计一个算法来计算你所能获取的最大利润。

注意：你不能在买入股票前卖出股票。
 */
 func maxProfit(prices []int) int {
    if prices == nil || len(prices) == 0{
        return 0
    }

    max := 0
    
    for from:=0;from <len(prices);  from++{
        for to := from +1;to < len(prices); to ++{
            if max < prices[to] -prices[from] -  {
                max = prices[from] - prices[to]
            }
        }
        
    }
}
 
 
```
