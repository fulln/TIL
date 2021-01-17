## 前 K 个高频元素

给定一个非空的整数数组，返回其中出现频率前 k 高的元素。

 

示例 1:

输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
示例 2:

输入: nums = [1], k = 1
输出: [1]
 

提示：

你可以假设给定的 k 总是合理的，且 1 ≤ k ≤ 数组中不相同的元素的个数。
你的算法的时间复杂度必须优于 O(n log n) , n 是数组的大小。
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的。
你可以按任意顺序返回答案。

作者：力扣 (LeetCode)
链接：https://leetcode-cn.com/leetbook/read/top-interview-questions-medium/xvzpxi/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

```go
func topKFrequent(nums []int, k int) []int {

    if len(nums) == 0{
        return nil
    }

    maps := make(map[int]int)

    for i:=0;i< len(nums);i++{
        maps[nums[i]] +=1
    }

    results := [][]int{}

    resp := []int{}

    for k,v := range maps{
        results= append(results,[]int{k,v})
    }
    
    qsort(0,len(results)-1,results)

    for i:=len(results)-1; i>= k-1 ;i--{
        resp = append(resp,results[i][0])
    }

    return resp

}

//手写快排,需要改动以便适配题目
func qsort(from,to int,res [][]int){
    begin := from
    end := to
    index := from
    if from >= to{
        return
    }

    for begin < end{
        for begin < end{
            if res[index][1] <= res[end][1]{
                end -- 
                continue
            }            
            res[index] ,res[end] = res[end],res[index]
            index =  end
            break
        }

        for begin < end{
            if res[index][1] >= res[begin][1]{
                begin ++ 
                continue
            }            
            res[index] ,res[begin] = res[begin],res[index]
            index =  begin
            break
        }
    }

    qsort(from,index-1,res)
    qsort(index+1,to,res)

}

```
