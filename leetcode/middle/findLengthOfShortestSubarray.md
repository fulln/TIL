##  1574. 删除最短的子数组使剩余数组有序

给你一个整数数组 arr ，请你删除一个子数组（可以为空），使得 arr 中剩下的元素是 非递减 的。

一个子数组指的是原数组中连续的一个子序列。

请你返回满足题目要求的最短子数组的长度。

 

示例 1：

输入：arr = [1,2,3,10,4,2,3,5]
输出：3
解释：我们需要删除的最短子数组是 [10,4,2] ，长度为 3 。剩余元素形成非递减数组 [1,2,3,3,5] 。
另一个正确的解为删除子数组 [3,10,4] 。
示例 2：

输入：arr = [5,4,3,2,1]
输出：4
解释：由于数组是严格递减的，我们只能保留一个元素。所以我们需要删除长度为 4 的子数组，要么删除 [5,4,3,2]，要么删除 [4,3,2,1]。
示例 3：

输入：arr = [1,2,3]
输出：0
解释：数组已经是非递减的了，我们不需要删除任何元素。
示例 4：

输入：arr = [1]
输出：0
 

提示：

1 <= arr.length <= 10^5
0 <= arr[i] <= 10^9

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/shortest-subarray-to-be-removed-to-make-array-sorted
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func findLengthOfShortestSubarray(arr []int) int {

    // 1. 删除的数组最短

    // 2. 需要删除一个连续子数组

    // 3. 删除后剩下的数据可以达到有序

    // => 1. f(n) 有序，n+1 > n, f(n+1) 有序

    // 2. 只能删除1次而且保证删除之后 后面的数组有序 有个方法判断当前数组是否有序？ 可以缓存 如f(n)(m) 有序，则f(n)(m+1) 有序当 m+1 > m 时 

    n := len(arr) -1    

    ret := n

    // 判断最后的数组的有序性

    last := arr[n]

    lasti := n

    for i:= n;i>=0;i--{

        if last >= arr[i]{

            lasti = i

            last = arr[i]

        }else{

            break

        }

    }

    if lasti == 0 {

        return 0

    }

    first := arr[0]

    firsti := 0 

    for i:=0;i < lasti;i++{

        if arr[i] >= first{

            first = arr[i]

            firsti = i

        }else{

            break

        }

    }

    if last == first {

        return lasti - firsti

    }else {

        temp1 := lasti

        for temp1 <= n {

            if arr[temp1] < first {

                temp1++

                continue

            }else{

                break

            }

        }

        ret= min(ret, temp1- firsti + 2)

        temp2 := firsti

        for temp2 >= 0 {

            if arr[temp2] > last {

                temp2--

                continue

            }else{

                break

            }

        }

        ret= min(ret,lasti - temp2-2)

    }

  

    return ret

}

  

func min(a,b int)int{

    if a < b {

        return a

    }else{

        return b

    }

}
```