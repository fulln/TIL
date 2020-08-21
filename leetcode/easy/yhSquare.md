## 杨辉三角

```go
/**
 杨辉三角
给定一个非负整数 numRows，生成杨辉三角的前 numRows 行。
 */
func generate(numRows int) [][]int {
    returns := [][]int{}

    if numRows == 0{
        return returns
    }

    index := []int{}

    for i :=0;i<numRows;i++{
        if len(index) == 0{
            index = append(index,1)
            returns = append(returns,index)
            continue
        }
        var news []int 
        for j:=0;j<=len(index);j++{        
            before := 0
            after := 0
            if  0 <=  j && j < len(index){
               before = index[j]
            }

            if  0 <=  j -1 && j-1 < len(index){
                after = index[j -1]
            }
            news =append(news,before+after)
        }    
        index = news
        returns = append(returns,index)   
    }
    return returns
}
```
