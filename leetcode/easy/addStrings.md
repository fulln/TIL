## 字符串相加

给定两个字符串形式的非负整数 num1 和num2 ，计算它们的和。

 

提示：

num1 和num2 的长度都小于 5100
num1 和num2 都只包含数字 0-9
num1 和num2 都不包含任何前导零
你不能使用任何內建 BigInteger 库， 也不能直接将输入的字符串转换为整数形式


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/add-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func addStrings(num1 string, num2 string) string {
    sum := 0
    returns := ""  
    for i,j:=len(num1)-1,len(num2)-1;i >=0 || j >=0 ;i,j = i-1,j-1{
        if i >= 0 {
            sum += int(num1[i] - '0') 
        }
       
        if j >= 0 {
            sum += int(num2[j] - '0') 
        }
        
        left := sum % 10
        sum = sum / 10
        returns = strconv.Itoa(left) +returns
    }

        if sum != 0{
            returns = strconv.Itoa(sum) + returns
        }
    

    return returns;
}

```