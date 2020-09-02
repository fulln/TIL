## 阶乘后的零

给定一个整数 n，返回 n! 结果尾数中零的数量。

```go
func trailingZeroes(n int) int {

    if(n < 5){
        return 0
    }
             
    return n/5 + trailingZeroes(n/5)
}
```
