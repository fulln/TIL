## 472. Concatenated Words

Given an array of strings words (without duplicates), return all the concatenated words in the given list of words.

A concatenated word is defined as a string that is comprised entirely of at least two shorter words in the given array.

 

Example 1:

Input: words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]
Output: ["catsdogcats","dogcatsdog","ratcatdogcat"]
Explanation: "catsdogcats" can be concatenated by "cats", "dog" and "cats"; 
"dogcatsdog" can be concatenated by "dog", "cats" and "dog"; 
"ratcatdogcat" can be concatenated by "rat", "cat", "dog" and "cat".
Example 2:

Input: words = ["cat","dog","catdog"]
Output: ["catdog"]
 

Constraints:

1 <= words.length <= 104
1 <= words[i].length <= 30
words[i] consists of only lowercase English letters.
All the strings of words are unique.
1 <= sum(words[i].length) <= 105

```go

func findAllConcatenatedWordsInADict(words []string) []string {
   maps := make(map[string]bool)
   for _,val := range words{
       maps[val]= true
   }
   ret := []string{}
   
   for _,val :=range words{
       l := len(val)
       // 将每一个单词进行计算看是否拼得出来
       dp := make([]bool,l+1)
       dp[0] = true
       for i:=1;i<= l;i++{
           m:= 0
           if i == l{
               m = 1
           }
           for j:=m;!dp[i] && j<i;j++{
               dp[i] = dp[j] && maps[val[j:i]]
           }
       }
       if dp[l]{
           ret = append(ret,val)
       }
   }

   return ret

   
}
```
