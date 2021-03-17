## 盛最多水的容器

给你 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点 (i, ai) 。在坐标内画 n 条垂直线，垂直线 i 的两个端点分别为 (i, ai) 和 (i, 0) 。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/container-with-most-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//双指针
func maxArea(height []int) int {
    max := 0
    for from,end :=0,len(height)-1;end >= 0 && from <len(height);{
        cur := min(height[from],height[end]) * (end - from)
        if max < cur{
            max =cur
        }

        if height[from] < height[end]{
            from ++
        }else{
            end --
        }
    }
    return max
}

func min(a,b int)int{
    if a< b{
        return a
    }else{
        return b
    }
}
```
