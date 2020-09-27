## 判定字符是否唯一
实现一个算法，确定一个字符串 s 的所有字符是否全都不同。

示例 1：

输入: s = "leetcode"
输出: false 
示例 2：

输入: s = "abc"
输出: true
限制：

0 <= len(s) <= 100
如果你不使用额外的数据结构，会很加分。
```go
//简单的冒泡思路
func isUnique(astr string) bool {

    for i:=0;i<len(astr);i++{
        for j:=i+1;j<len(astr);j++{
            if astr[j]  == astr[i]{
                return false
            }
        }    
    }

    return true

}
//位运算思路
func isUnique(astr string) bool {
	var sum uint32  = 0
	for _,val := range astr{
		modest := uint32(val - 'a')
		if sum & (1 <<modest) != 0{
			return false
		}else{
			sum =sum| (1<< modest)
		}
	}
	return true
}
//快排
```
