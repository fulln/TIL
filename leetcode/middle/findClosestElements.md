## . 找到 K 个最接近的元素

给定一个 排序好 的数组 arr ，两个整数 k 和 x ，从数组中找到最靠近 x（两数之差最小）的 k 个数。返回的结果必须要是按升序排好的。

整数 a 比整数 b 更接近 x 需要满足：

|a - x| < |b - x| 或者
|a - x| == |b - x| 且 a < b
 

示例 1：

输入：arr = [1,2,3,4,5], k = 4, x = 3
输出：[1,2,3,4]
示例 2：

输入：arr = [1,2,3,4,5], k = 4, x = -1
输出：[1,2,3,4]

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/find-k-closest-elements
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func findClosestElements(arr []int, k int, x int) []int {
    left :=0
    min := 10001
    for i,val :=range arr{
        if abs(val,x) < min{
            min = abs(val,x)
            left = i  
        }
    }

    ret := []int{arr[left]}
    l,r,size := 1,1,1
    for size < k  {        
        size ++
        if left + r == len(arr) {            
            ret = append([]int{arr[left -l]},ret[:]...)
            l++
            continue
        }

        if left - l == -1 {            
            ret = append(ret,arr[left + r])
            r++
            continue
        }

        if abs(arr[left -l] ,x) > abs(arr[left +r],x){            
            ret = append(ret,arr[left +r])
            r++
        }else{            
            ret = append([]int{arr[left -l]},ret[:]...)
            l++
        }
        
    } 
    return ret
}

func abs(a,b int)int{
    if a > b{
        return a -b
    }else{
        return b -a
    }
}

func findClosestElements(arr []int, k int, x int) []int {
    left,right :=0,len(arr)-k
    for left < right{
        middle := (left +right) /2
        if x - arr[middle] > arr[middle + k] -x {
            left = middle +1
        } else{
            right = middle
        }
    }

    return arr[left:left+k]
}

```
