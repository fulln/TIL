## 颜色分类

给定一个包含红色、白色和蓝色，一共 n 个元素的数组，原地对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。

此题中，我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。

注意：请不要使用代码库中的排序函数来解决这道题。

 

进阶：

你能想出一个仅使用常数空间的一趟扫描算法吗？
 

示例 1：

输入：nums = [2,0,2,1,1,0]
输出：[0,0,1,1,2,2]
示例 2：

输入：nums = [2,0,1]
输出：[0,1,2]
示例 3：

输入：nums = [0]
输出：[0]
示例 4：

输入：nums = [1]
输出：[1]

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvg25c/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```go
//O(n) 常量空间
func sortColors(nums []int)  {

    begin,last, now:=0,len(nums)-1,0
    for now <= last{
        if nums[now] == 0{         
            nums[begin],nums[now] = nums[now],nums[begin]        
            begin++   
            now ++     
            continue
        }

        if nums[now] == 1{
            now++
            continue
        }

        
        if nums[now] == 2{
            nums[last],nums[now] = nums[now],nums[last]            
            last-- 
        }
    } 
}

```
