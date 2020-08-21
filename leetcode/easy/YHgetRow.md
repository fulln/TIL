##  杨辉三角II 

```go
/**
给定一个非负索引 k，其中 k ≤ 33，返回杨辉三角的第 k 行。
 */
func getRow1(rowIndex int) []int {
 
    index := []int{}


    for i :=0;i<rowIndex+1;i++{
        if len(index) == 0{
            index = append(index,1)
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
           
    }
    return index


}

func getRow2(rowIndex int) []int {
   rowIndex ++
   index := []int{1}
   for i :=1; i < rowIndex ;i++{
        nums :=int(index[i-1] * (rowIndex -i) /i)
        index =append(index,nums)
   }
   return index
}


```
