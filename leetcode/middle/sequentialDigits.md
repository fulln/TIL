## 顺次数

我们定义「顺次数」为：每一位上的数字都比前一位上的数字大 1 的整数。

请你返回由 [low, high] 范围内所有顺次数组成的 有序 列表（从小到大排序）。

 

示例 1：

输出：low = 100, high = 300
输出：[123,234]
示例 2：

输出：low = 1000, high = 13000
输出：[1234,2345,3456,4567,5678,6789,12345]
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/sequential-digits
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func sequentialDigits(low int, high int) []int {
    c := counts(low)
    f := first(low,c)
    flag := false
    nums := []int{}
    for{
        curr := f
        sum := c
        total := curr
        for ;sum>0;sum --{
            curr = curr+1
            if curr == 10{
                c++
                f = 1
                flag = true
                break                  
            }else{
                flag =false
                total = total*10+curr
            }
        }

        if flag {
            continue
        }

        if total >= low && total <= high{
            nums= append(nums,total)
            f++
        }
        if total > high{
            break
        }
        if total < low{
            break
        }
    }
   
        

       return nums
}


func first(a ,c int) int{
    f := 1
    for ;c >0;c--{
        f = f * 10
    }
    return int(a/f)
} 



func counts(a int)int{
    count := 0
    for a >= 10 {
        a = a/10
        count ++
    }
    return count
}
//逆思维
func sequentialDigits(low int, high int) []int {

    res := []int{}

    for i:=1;i<=9;i++{
        sum := i
        for j:= i+1 ;j<=9;j++{
            sum =sum*10 +j
            if  low <= sum && sum <= high{
                res =append(res,sum)
            }            
             if sum > high{
                    break;
            }

        }

    }
    sort.Ints(res)
    return res
}

```
