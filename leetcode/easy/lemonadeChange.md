## 860. 柠檬水找零

在柠檬水摊上，每一杯柠檬水的售价为 5 美元。

顾客排队购买你的产品，（按账单 bills 支付的顺序）一次购买一杯。

每位顾客只买一杯柠檬水，然后向你付 5 美元、10 美元或 20 美元。你必须给每个顾客正确找零，也就是说净交易是每位顾客向你支付 5 美元。

注意，一开始你手头没有任何零钱。

如果你能给每位顾客正确找零，返回 true ，否则返回 false 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/lemonade-change
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func lemonadeChange(bills []int) bool {
    maps := make(map[int]int)
    for _,i := range bills{
        if i == 10{
            if maps[5] == 0{
                return false
            }
            maps[5] = maps[5] -1
            maps[10] =maps[10] +1
        }

        if i == 5{
             maps[5] = maps[5] + 1
        }

         if i == 20{
            if maps[10] >= 1{
                maps[10] =maps[10] - 1
                if maps[5] < 1{
                    return false
                }
                maps[5] = maps[5] - 1
            }else {
                if maps[5] < 3{
                    return false
                }
                maps[5] = maps[5] -3
            }
        }


    }
    return true


}
```
