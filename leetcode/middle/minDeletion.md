## 美化数组的最少删除数

func minDeletion(nums []int) int {
    
    
    ret := 0
    for i:=0;i< len(nums)-1;i++{
        if (i - ret)  % 2 == 0{
            if nums[i] == nums[i +1]{
                ret ++    
            }
        }
    }
    
    if (len(nums)- ret) & 1 == 1{
       ret ++
    }
    
    
    return ret
}
