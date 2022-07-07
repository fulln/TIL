##  单词替换

在英语中，我们有一个叫做 词根(root) 的概念，可以词根后面添加其他一些词组成另一个较长的单词——我们称这个词为 继承词(successor)。例如，词根an，跟随着单词 other(其他)，可以形成新的单词 another(另一个)。

现在，给定一个由许多词根组成的词典 dictionary 和一个用空格分隔单词形成的句子 sentence。你需要将句子中的所有继承词用词根替换掉。如果继承词有许多可以形成它的词根，则用最短的词根替换它。

你需要输出替换之后的句子。

 

示例 1：

输入：dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
输出："the cat was rat by the bat"
示例 2：

输入：dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
输出："a a b c"

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/replace-words
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func replaceWords(dictionary []string, sentence string) string {
    type trie map[rune]trie
    root := trie{}
    for _, s := range dictionary {
        cur := root
        for _, c := range s {
            if cur[c] == nil {
                cur[c] = trie{}
            }
            cur = cur[c]
        }
        cur['#'] = trie{}
    }

    words := strings.Split(sentence, " ")
    for i, word := range words {
        cur := root
        for j, c := range word {
            if cur['#'] != nil {
                words[i] = word[:j]
                break
            }
            if cur[c] == nil {
                break
            }
            cur = cur[c]
        }
    }
    return strings.Join(words, " ")
}

```
