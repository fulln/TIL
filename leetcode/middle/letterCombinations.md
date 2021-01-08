## 电话号码的字母组合

给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。



示例:

输入："23"
输出：["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go


var phoneMap map[string]string = map[string]string{
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}

func letterCombinations(digits string) []string {
    returns := []string{}

    for i:=0;i<len(digits);i++{
        new := []string{}
        l := len(phoneMap[string(digits[i])])
        for j:=0 ;j< l;j++{
            if len(returns) >0{
                for m:= 0;m< len(returns);m++{
                new = append(new, returns[m]+string(phoneMap[string(digits[i])][j]))
                }
            }else{
                new = append(new,string(phoneMap[string(digits[i])][j]))
            }            
        }
        returns = new 
    }
  return returns
}

func letterCombinations(digits string) []string {
    

    ans :=[]string{}

    
    if digits == ""{
        return ans
    }

    var dsf func(int,string)

    dsf = func(i int,dis string){
        if i == len(digits){
            ans = append(ans,dis)
            return
        }

        for _,m := range(phoneMap[string(digits[i])]){
            dsf(i+1,dis+string(m))
        }

    }

    dsf(0,"")

    return ans

}
```
