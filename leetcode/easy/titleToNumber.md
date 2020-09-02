##  Excel表列序号

给定一个Excel表格中的列名称，返回其相应的列序号。

```go

func titleToNumber(s string) int {
	sum:= 0
	for i:=0 ;i< len(s) ;i++{
		sum = sum*26 + int(s[i]) -64
	}
	return sum

}

```
