## 恢复空格

哦，不！你不小心把一个长篇文章中的空格、标点都删掉了，并且大写也弄成了小写。像句子"I reset the computer. It still didn’t boot!"已经变成了"iresetthecomputeritstilldidntboot"。在处理标点符号和大小写之前，你得先把它断成词语。当然了，你有一本厚厚的词典dictionary，不过，有些词没在词典里。假设文章用sentence表示，设计一个算法，把文章断开，要求未识别的字符最少，返回未识别的字符数。

注意：本题相对原题稍作改动，只需返回未识别的字符数

 

示例：

输入：
dictionary = ["looked","just","like","her","brother"]
sentence = "jesslookedjustliketimherbrother"
输出： 7
解释： 断句后为"jess looked just like tim her brother"，共7个未识别字符。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/re-space-lcci
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func respace(dictionary []string, sentence string) int {
    // 状态转移方程就是
    //当前最少识别 =  长度- 最多识别数
    //最多识别数 
    // 如果当前  + w 能识别
    // f[i][j] = f[i - dictionary[w]][j] + len(dictionary[w]) 
    // 如果当前不能识别
    // f[i][j] = f[i-1][j]
    // 如果长度等于0
    //f[0][0] = 0
    n := len(dictionary)

    dp :=make([]int,n+1)

    for  i:=1;i <=n;i++ {
            for _,val := range dictionary{
                m:= len(val)
                if i>= m && sentence[i-m:i] == val{
                    dp[i] = max(dp[i],dp[i-m] + m)
                }else{
                    dp[i]  = max(dp[i],dp[i-1])
                }
        } 
    }
    return n - dp[n]
}

func max(a,b int)int{
    if a >b{
        return a
    }else{
        return b
    }
}

//java 可行  golang不可行?
class Solution {
    public int respace(String[] dictionary, String sentence) {
        int m = sentence.length();
        int[] dp = new int[m+1];
        for(int i=1;i<=m;i++){                 //外层循环字符串
            for(String word:dictionary){             //内层循环字典
                int len = word.length();
                if(i >= len && word.equals(sentence.substring(i-len,i))){
                    dp[i] = Math.max(dp[i],dp[i-len]+len);  //状态转移
                }else{
                    dp[i] = Math.max(dp[i],dp[i-1]);
                }
            }
        }
        return m-dp[m];
    }
}
```
