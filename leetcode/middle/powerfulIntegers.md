---
dg-publish: true
title： powerfulIntegers
createTime: 2023-05-02 22:24  
---

#### [970. 强整数](https://leetcode.cn/problems/powerful-integers/)

给定三个整数 x 、 y 和 bound ，返回 值小于或等于 bound 的所有 强整数 组成的列表 。

如果某一整数可以表示为 xi + yj ，其中整数 i >= 0 且 j >= 0，那么我们认为该整数是一个 强整数 。

你可以按 任何顺序 返回答案。在你的回答中，每个值 最多 出现一次。

 

示例 1：

输入：x = 2, y = 3, bound = 10
输出：[2,3,4,5,7,9,10]
解释： 
2 = 20 + 30
3 = 21 + 30
4 = 20 + 31
5 = 21 + 31
7 = 22 + 31
9 = 23 + 30
10 = 20 + 32
示例 2：

输入：x = 3, y = 5, bound = 15
输出：[2,4,6,8,10,14]
 

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/powerful-integers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func powerfulIntegers(x int, y int, bound int) []int {

    res := make(map[int]bool)

    lx := 1

    for i:=0;i< 30;i++{

        ly := 1

        for j:=0;j< 30;j++{            

            value := lx+ly 

            if value > bound {

                break

            }else{

                res[value] = true

            }

  

            ly *= y

        }

        if lx > bound {

            break

        }

  

        lx *= x

    }

    ret := []int{}

    for k := range res {

        ret =append(ret,k)

    }

    return ret

}
```