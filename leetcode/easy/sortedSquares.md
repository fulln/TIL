## 有序数组的平方

给定一个按非递减顺序排序的整数数组 A，返回每个数字的平方组成的新数组，要求也按非递减顺序排序。

 

示例 1：

输入：[-4,-1,0,3,10]
输出：[0,1,9,16,100]
示例 2：

输入：[-7,-3,2,3,11]
输出：[4,9,9,49,121]
 

提示：

1 <= A.length <= 10000
-10000 <= A[i] <= 10000
A 已按非递减顺序排序。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/squares-of-a-sorted-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func sortedSquares(A []int) []int {
    //快速排序
    quickSort(A, 0, len(A)-1)
      for i:=0;i <len(A);i++{
          A[i] = A[i]*A[i]
      }
    return A
}
func quickSort(arr []int,first,last int){
    flag := first
	left := first
	right := last

    if first >= last {
		return 
	}

    for first < last{
        for first < last {
            if arr[last] >= arr[flag] {
				last--
				continue
			}
            // 交换数据
			arr[last], arr[flag] = arr[flag], arr[last]
			flag = last
			break
        }
        for first < last {
			if arr[first] <= arr[flag]{
				first++
				continue
			}
			arr[first], arr[flag] = arr[flag], arr[first]
			flag = first
			break
		}
    }
    quickSort(arr, left, flag-1)
	quickSort(arr, flag+1, right)
}
```
