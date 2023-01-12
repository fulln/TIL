## 1803. 统计异或值在范围内的数对有多少
给你一个整数数组 nums （下标 从 0 开始 计数）以及两个整数：low 和 high ，请返回 漂亮数对 的数目。

漂亮数对 是一个形如 (i, j) 的数对，其中 0 <= i < j < nums.length 且 low <= (nums[i] XOR nums[j]) <= high 。

 

示例 1：

输入：nums = [1,4,2,7], low = 2, high = 6
输出：6
解释：所有漂亮数对 (i, j) 列出如下：
    - (0, 1): nums[0] XOR nums[1] = 5 
    - (0, 2): nums[0] XOR nums[2] = 3
    - (0, 3): nums[0] XOR nums[3] = 6
    - (1, 2): nums[1] XOR nums[2] = 6
    - (1, 3): nums[1] XOR nums[3] = 3
    - (2, 3): nums[2] XOR nums[3] = 5
示例 2：

输入：nums = [9,8,4,2,1], low = 5, high = 14
输出：8
解释：所有漂亮数对 (i, j) 列出如下：
​​​​​    - (0, 2): nums[0] XOR nums[2] = 13
    - (0, 3): nums[0] XOR nums[3] = 11
    - (0, 4): nums[0] XOR nums[4] = 8
    - (1, 2): nums[1] XOR nums[2] = 12
    - (1, 3): nums[1] XOR nums[3] = 10
    - (1, 4): nums[1] XOR nums[4] = 9
    - (2, 3): nums[2] XOR nums[3] = 6
    - (2, 4): nums[2] XOR nums[4] = 5
 

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/count-pairs-with-xor-in-a-range
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func countPairs(nums []int, low int, high int) int {
    sum := 0 
    xor := 0
    for i:=0;i< len(nums);i++{
        xor = xor ^ nums[i] 
        for j:=i+1;j< len(nums);j++{
            xor = xor ^ nums[j]            
            if xor >= low && xor <= high{
                sum += 1
            }
            xor = xor ^ nums[j]
        }
        xor = xor ^ nums[i] 
    }

    return sum

}
```