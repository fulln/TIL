##  换酒问题

```go
/**
小区便利店正在促销，用 numExchange 个空酒瓶可以兑换一瓶新酒。你购入了 numBottles 瓶酒。

如果喝掉了酒瓶中的酒，那么酒瓶就会变成空的。

请你计算 最多 能喝到多少瓶酒。
 */
func numWaterBottles(numBottles int, numExchange int) int {

    if  numBottles < 1 {
        return 0
    }

    return   numBottles + getusedButton(numBottles,numExchange) 

}

func getusedButton(numBottles int, numExchange int)int{

    if  numBottles < 1 {
        return 0
    }

    if  numBottles < numExchange {
        return 0
    }

    left :=  numBottles % numExchange
    one := numBottles / numExchange

    return int(one) + getusedButton(one+left,numExchange) 

} 
 
 
```
