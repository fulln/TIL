## 划分数组为连续数字的集合
给你一个整数数组 nums 和一个正整数 k，请你判断是否可以把这个数组划分成一些由 k 个连续数字组成的集合。
如果可以，请返回 True；否则，返回 False。

 

注意：此题目与 846 重复：https://leetcode-cn.com/problems/hand-of-straights/

 

示例 1：

输入：nums = [1,2,3,3,4,4,5,6], k = 4
输出：true
解释：数组可以分成 [1,2,3,4] 和 [3,4,5,6]。
示例 2：

输入：nums = [3,2,1,2,3,4,3,4,5,9,10,11], k = 3
输出：true
解释：数组可以分成 [1,2,3] , [2,3,4] , [3,4,5] 和 [9,10,11]。
示例 3：

输入：nums = [3,3,2,2,1,1], k = 3
输出：true
示例 4：

输入：nums = [1,2,3,4], k = 3
输出：false
解释：数组不能分成几个大小为 3 的子数组。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/divide-array-in-sets-of-k-consecutive-numbers
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
class Solution {
public:
    bool isNStraightHand(vector<int>& hand, int W) {
        // 如果数量无法整除，直接返回失败
        if (hand.size() % W > 0)
        {
            return false;
        }
        //  默认是从小到大
        map<int, int> maps;
        for (int num : hand)
        {
            ++maps[num];
        }

        // 从小到大开始遍历
        for (auto iter = maps.begin(); iter != maps.end(); ++iter)
        {
            // 只有计数》0需要考虑
            if (iter->second > 0)
            {
                // auto currIter = iter;
                // ++currIter;
                for (int i = 1; i < W; ++i)
                {
                    // 只有没到结束，同时对应的数字计数器满足对应的数量
                    int next = iter->first + i;
                    // cout << iter->first << " " << iter->second << " minus " << next << " " << maps[next] << endl;
                    if (maps.find(next) != maps.end() && maps[next] >= iter->second)
                    {
                        maps[next] -= iter->second;
                    }
                    else
                    {
                        // 不满足情况 直接返回失败
                        return false;
                    }
                }
            }
        }

        // 默认返回成功
        return true;
    }
};

作者：ffreturn
链接：https://leetcode-cn.com/problems/hand-of-straights/solution/846-ctong-su-yi-dong-de-mapjie-fa-by-ffr-n12i/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```
