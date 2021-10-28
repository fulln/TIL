## 重新排序得到 2 的幂
给定正整数 N ，我们按任何顺序（包括原始顺序）将数字重新排序，注意其前导数字不能为零。

如果我们可以通过上述方式得到 2 的幂，返回 true；否则，返回 false。

 

示例 1：

输入：1
输出：true
示例 2：

输入：10
输出：false
示例 3：

输入：16
输出：true
示例 4：

输入：24
输出：false
示例 5：

输入：46
输出：true

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reordered-power-of-2
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func isPowerOfTwo(n int) bool {
    return n&(n-1) == 0
}

func reorderedPowerOf2(n int) bool {
    nums := []byte(strconv.Itoa(n))
    sort.Slice(nums, func(i, j int) bool { return nums[i] < nums[j] })

    m := len(nums)
    vis := make([]bool, m)
    var backtrack func(int, int) bool
    backtrack = func(idx, num int) bool {
        if idx == m {
            return isPowerOfTwo(num)
        }
        for i, ch := range nums {
            // 不能有前导零
            if num == 0 && ch == '0' || vis[i] || i > 0 && !vis[i-1] && ch == nums[i-1] {
                continue
            }
            vis[i] = true
            if backtrack(idx+1, num*10+int(ch-'0')) {
                return true
            }
            vis[i] = false
        }
        return false
    }
    return backtrack(0, 0)
}
```

