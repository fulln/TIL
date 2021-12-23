## 绝对值表达式的最大值
给你两个长度相等的整数数组，返回下面表达式的最大值：

|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|

其中下标 i，j 满足 0 <= i, j < arr1.length。

 

示例 1：

输入：arr1 = [1,2,3,4], arr2 = [-1,4,5,6]
输出：13
示例 2：

输入：arr1 = [1,-2,-5,0,10], arr2 = [0,-2,-1,-7,-4]
输出：20
 

提示：

2 <= arr1.length == arr2.length <= 40000
-10^6 <= arr1[i], arr2[i] <= 10^6

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/maximum-of-absolute-value-expression
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func maxAbsValExpr(arr1 []int, arr2 []int) int {

     maxA,minA,maxB,minB,maxC,minC,maxD,minD := -1000000,1000000,-1000000,1000000,-1000000,1000000,-1000000,1000000

     for i:= 0;i< len(arr1);i++{
         maxA = max(maxA,arr1[i]+arr2[i]+i)
         maxB = max(maxB,-arr1[i]+arr2[i]+i)
         maxC = max(maxC,arr1[i]-arr2[i]+i)
         maxD = max(maxD,arr1[i]+arr2[i]-i)
         minA = min(minA,arr1[i]+arr2[i]+i)
         minB = min(minB,-arr1[i]+arr2[i]+i)
         minC = min(minC,arr1[i]-arr2[i]+i)
         minD = min(minD,arr1[i]+arr2[i]-i)
     }

     return max(max(maxA-minA,maxB-minB),max(maxC-minC,maxD-minD));

}

func max(a,b int)int{
    if a > b{
        return a
    }else{
        return b
    }
}


func min(a,b int)int{
    if a < b{
        return a
    }else{
        return b
    }
}
```
