## 剑指 Offer 40. 最小的k个数

输入整数数组 arr ，找出其中最小的 k 个数。例如，输入4、5、1、6、2、7、3、8这8个数字，则最小的4个数字是1、2、3、4。

 

示例 1：

输入：arr = [3,2,1], k = 2
输出：[1,2] 或者 [2,1]
示例 2：

输入：arr = [0,1,2,1], k = 1
输出：[0]
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/zui-xiao-de-kge-shu-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
//冒泡破一切
func getLeastNumbers(arr []int, k int) []int {

	if k == 0{
		return []int{}
	}
	for i:=0;i<len(arr);i++{
		for j:=0;j< len(arr) -i -1;j++{
			if arr[j] >arr[j+1]{
				arr[j],arr[j+1] =arr[j+1],arr[j]
			}
		}
	}
	return arr[:k]
}
//快排模板要牢记
func getLeastNumbers(arr []int, k int) []int {

	if k == 0{
		return []int{}
	}
	return quickSort(arr)[:k]
}

func quickSort(arr []int) (res []int) {
	// 剩下一个元素则直接跳出递归
	if len(arr) < 2 {
		return arr
	}
	// 直接取第一个元素为基准值
	pivot := arr[0]

	// 初始化变量，left表示小于基准值，middle表示和基准值一样的元素，right表示大于基准值的元素
	var left, middle, right []int

	// 遍历数组
	for _, v := range arr {
		// 小于基准值的放左边，等于的放中间，大于的放右边
		if v < pivot {
			left = append(left, v)
		} else if v == pivot {
			middle = append(middle, v)
		} else if v > pivot {
			right = append(right, v)
		}
	}
	// 递归调用此方法，直至数组全部排序完毕
	return append(append(quickSort(left[:]), middle...), quickSort(right[:])...)
}

```
