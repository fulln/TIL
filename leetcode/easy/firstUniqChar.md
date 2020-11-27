## 字符串中的第一个唯一字符


给定一个字符串，找到它的第一个不重复的字符，并返回它的索引。如果不存在，则返回 -1。

 

示例：

s = "leetcode"
返回 0

s = "loveleetcode"
返回 2

```go
func firstUniqChar(s string) int {
    maps := make(map[byte]int)

    for i:= 0;i< len(s);i++{
        maps[s[i]] += 1
    }

    for i:= 0;i< len(s);i++{
        if maps[s[i]] == 1{
            return i
        }
    }

    return -1
}
```
