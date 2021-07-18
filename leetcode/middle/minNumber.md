## 把数组排成最小的数

输入一个非负整数数组，把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。

 

示例 1:

输入: [10,2]
输出: "102"
示例 2:

输入: [3,30,34,5,9]
输出: "3033459"
 

提示:

0 < nums.length <= 100
说明:

输出结果可能非常大，所以你需要返回一个字符串而不是整数
拼接起来的数字可能会有前导 0，最后结果不需要去掉前导 0

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go


func minNumber(nums []int) string {
    quickSort(nums,0,len(nums)-1)
    var sum string
    for _,val := range nums{ 
        sum += strconv.Itoa(val)
    }
    return sum
}

func quickSort(nums []int,from,to int){

   if from >= to {
		return 
	}
    begin := from
    end := to
    middle := from
    for from < to{
        
        for from < to{
            if compare(nums[middle],nums[to]){
                to--
                continue
            }
            nums[middle],nums[to] =  nums[to],nums[middle]
            middle = to
            break
        }

        for from < to{
            if compare(nums[from],nums[middle]){
                from++
                continue
            }
            nums[from],nums[middle] =  nums[middle],nums[from]
            middle = from
            break
        }
    }

    quickSort(nums,begin,middle-1)
    
    quickSort(nums,middle+1,end)


}

func compare(a,b int)bool{
    one := strconv.Itoa(a) +strconv.Itoa(b)
	two := strconv.Itoa(b) + strconv.Itoa(a)

    if one <= two{
        return true
    }else{
        return false
    }
}
```
