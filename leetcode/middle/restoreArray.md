## 从相邻元素对还原数组
存在一个由 n 个不同元素组成的整数数组 nums ，但你已经记不清具体内容。好在你还记得 nums 中的每一对相邻元素。

给你一个二维整数数组 adjacentPairs ，大小为 n - 1 ，其中每个 adjacentPairs[i] = [ui, vi] 表示元素 ui 和 vi 在 nums 中相邻。

题目数据保证所有由元素 nums[i] 和 nums[i+1] 组成的相邻元素对都存在于 adjacentPairs 中，存在形式可能是 [nums[i], nums[i+1]] ，也可能是 [nums[i+1], nums[i]] 。这些相邻元素对可以 按任意顺序 出现。

返回 原始数组 nums 。如果存在多种解答，返回 其中任意一个 即可。

 

示例 1：

输入：adjacentPairs = [[2,1],[3,4],[3,2]]
输出：[1,2,3,4]
解释：数组的所有相邻元素对都在 adjacentPairs 中。
特别要注意的是，adjacentPairs[i] 只表示两个元素相邻，并不保证其 左-右 顺序。
示例 2：

输入：adjacentPairs = [[4,-2],[1,4],[-3,1]]
输出：[-2,4,1,-3]
解释：数组中可能存在负数。
另一种解答是 [-3,1,4,-2] ，也会被视作正确答案。
示例 3：

输入：adjacentPairs = [[100000,-100000]]
输出：[100000,-100000]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/restore-the-array-from-adjacent-pairs
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func restoreArray(adjacentPairs [][]int) []int {

    // 首先用一个数组装对应的[]int
    // 遍历下  用个map指向他出现的另外一个int
    ret := make([]int,len(adjacentPairs) + 1)
    maps := make(map[int][]int, len(ret) )
    for _, val := range adjacentPairs {
        maps[val[0]] = append(maps[val[0]], val[1])
        maps[val[1]] = append(maps[val[1]], val[0])
    }
    
    for key,_ := range maps{
        level := maps[key]
        if len(level) == 1{
                ret[0] = key
                ret[1] = level[0]
                break
        }
    }

    index := 1

    for index < len(ret)-1 {
        lv := maps[ret[index]] 
        if len(lv) == 1{
            ret[len(ret)-1] = lv[0]
            continue
        }
        if lv[0] == ret[index-1] {
            ret[index+1] = lv[1]
        }else{
            ret[index+1] = lv[0]
        }
        index ++
    }

    return ret
    

}

```
