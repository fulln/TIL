## 查找和最小的 K 对数字
给定两个以 升序排列 的整数数组 nums1 和 nums2 , 以及一个整数 k 。

定义一对值 (u,v)，其中第一个元素来自 nums1，第二个元素来自 nums2 。

请找到和最小的 k 个数对 (u1,v1),  (u2,v2)  ...  (uk,vk) 。

 

示例 1:

输入: nums1 = [1,7,11], nums2 = [2,4,6], k = 3
输出: [1,2],[1,4],[1,6]
解释: 返回序列中的前 3 对数：
     [1,2],[1,4],[1,6],[7,2],[7,4],[11,2],[7,6],[11,4],[11,6]
示例 2:

输入: nums1 = [1,1,2], nums2 = [1,2,3], k = 2
输出: [1,1],[1,1]
解释: 返回序列中的前 2 对数：
     [1,1],[1,1],[1,2],[2,1],[1,2],[2,2],[1,3],[1,3],[2,3]
示例 3:

输入: nums1 = [1,2], nums2 = [3], k = 3 
输出: [1,3],[2,3]
解释: 也可能序列中所有的数对都被返回:[1,3],[2,3]
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/find-k-pairs-with-smallest-sums
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func kSmallestPairs(nums1 []int, nums2 []int, k int) [][]int {
    ans:=[][]int{} 
    for i:=0;i<len(nums1)&&i<k;i++{
        for j:=0;j<len(nums2)&&j<k;j++{
            ans=append(ans,[]int{nums1[i],nums2[j]})
        }
    }

    sort.Slice(ans,func(i,j int)bool{
        return ans[i][0]+ans[i][1]<ans[j][0]+ans[j][1]
    })
    if k<len(ans){
        return ans[:k]
    }
    return ans 
    
}
```
