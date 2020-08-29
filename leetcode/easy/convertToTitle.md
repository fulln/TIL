## Excel表列名称

给定一个正整数，返回它在 Excel 表中相对应的列名称。

例如，

    1 -> A
    2 -> B
    3 -> C
    ...
    26 -> Z
    27 -> AA
    28 -> AB 
    ...

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/excel-sheet-column-title
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func convertToTitle(n int)string {

	rest := n / 26
	left := n % 26

	var returns string

	if rest != 0{
		if rest >26{
			returns += convertToTitle(rest)
		}else{
			b := rune(64 + rest)
			returns  += string(b)
		}
	}

	if left == 0 {
		return returns;
	}

	c :=rune(64+left)
	return returns+string(c)
}
```
