## 1780. 判断一个数字是否可以表示成三的幂的和
给你一个整数 n ，如果你可以将 n 表示成若干个不同的三的幂之和，请你返回 true ，否则请返回 false 。

对于一个整数 y ，如果存在整数 x 满足 y == 3x ，我们称这个整数 y 是三的幂。

 

示例 1：

输入：n = 12
输出：true
解释：12 = 31 + 32
示例 2：

输入：n = 91
输出：true
解释：91 = 30 + 32 + 34
示例 3：

输入：n = 21
输出：false

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/check-if-number-is-a-sum-of-powers-of-three
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```java
class Solution {
    public boolean checkPowersOfThree(int n) {
        int sum = 1;
        int curr = 0;
        for (int i = 1; i < n ; i++) {
            sum *= 3  ;
            if (sum > n) {
                sum /=3;
                curr = i - 1;
                break;
            }
        }
        if (sum == n) {
            return true;
        }
        int temp = 0;
        for (int i = curr; i >= 0;  i--) {
            if (temp + sum > n ){
                sum /=3;
            }else if (temp + sum == n){
                return true;
            }else {
                temp += sum;
                sum /=3;
            }
        }
        return false;
    }
}

or

func checkPowersOfThree(n int) bool {
        for ; n > 0 ;{
            if n % 3 == 2{
                return false
            }
            n /=3
        }
        return true;
}

```
