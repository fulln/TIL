---
dg-publish: true
title: rearrangeBarcodes
createTime: 2023-05-14 23:13  
---
#### [1054. 距离相等的条形码](https://leetcode.cn/problems/distant-barcodes/)

难度中等164

在一个仓库里，有一排条形码，其中第 `i` 个条形码为 `barcodes[i]`。

请你重新排列这些条形码，使其中任意两个相邻的条形码不能相等。 你可以返回任何满足该要求的答案，此题保证存在答案。

**示例 1：**

**输入：**barcodes = [1,1,1,2,2,2]
**输出：**[2,1,2,1,2,1]

**示例 2：**

**输入：**barcodes = [1,1,1,1,2,2,3,3]
**输出：**[1,3,1,3,2,1,2,1]

**提示：**

-   `1 <= barcodes.length <= 10000`
-   `1 <= barcodes[i] <= 10000`
```go
func rearrangeBarcodes(barcodes []int) []int {
    if len(barcodes) < 2 {
        return barcodes
    }

    counts := make(map[int]int)
    for _, b := range barcodes {
        counts[b] = counts[b] + 1
    }

    evenIndex := 0
    oddIndex := 1
    halfLength := len(barcodes) / 2
    res := make([]int, len(barcodes))
    for x, count := range counts {
        for count > 0 && count <= halfLength && oddIndex < len(barcodes) {
            res[oddIndex] = x
            count--
            oddIndex += 2
        }
        for count > 0 {
            res[evenIndex] = x
            count--
            evenIndex += 2
        }
    }
    return res
}
```