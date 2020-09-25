## 剑指 Offer 05. 替换空格
请实现一个函数，把字符串 s 中的每个空格替换成"%20"。

 

示例 1：

输入：s = "We are happy."
输出："We%20are%20happy."

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ti-huan-kong-ge-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func replaceSpace(s string) string {
	scode :=[]rune{}
	for _,val:= range(s) {
		if val  == ' '{
			scode = append(scode,'%','2','0')
		}else {
			scode = append(scode,val)
		}
	}
	return string(scode)
}
//或者直接使用replace方法
```
