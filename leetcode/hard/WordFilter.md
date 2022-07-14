## 745. 前缀和后缀搜索

设计一个包含一些单词的特殊词典，并能够通过前缀和后缀来检索单词。

实现 WordFilter 类：

WordFilter(string[] words) 使用词典中的单词 words 初始化对象。
f(string pref, string suff) 返回词典中具有前缀 prefix 和后缀 suff 的单词的下标。如果存在不止一个满足要求的下标，返回其中 最大的下标 。如果不存在这样的单词，返回 -1 。
 

示例：

输入
["WordFilter", "f"]
[[["apple"]], ["a", "e"]]
输出
[null, 0]
解释
WordFilter wordFilter = new WordFilter(["apple"]);
wordFilter.f("a", "e"); // 返回 0 ，因为下标为 0 的单词：前缀 prefix = "a" 且 后缀 suff = "e" 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/prefix-and-suffix-search
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```java

class WordFilter {

    private DictTree order;
    private DictTree reverse;

    public WordFilter(String[] s) {
        order = new DictTree();
        reverse = new DictTree();
        for (int i = 0; i < s.length; i++) {
            order.add(s[i], i, true);
            reverse.add(s[i], i, false);
        }
    }

    public int f(String pref, String suff) {
        List<Integer> search = order.search(pref.toCharArray());
        char[] chars = new char[suff.length()];
        for (int i = 0; i < chars.length; i++) {
            chars[i] = suff.charAt(chars.length - 1 - i);
        }
        List<Integer> search1 = reverse.search(chars);
        if (search.size() == 0 || search1.size() == 0) {
            return -1;
        }

        for (int j = search1.size() - 1,i = search.size() - 1; i>=0 && j >= 0;) {
            if (search.get(i) > search1.get(j)) {
                i--;
            } else if (search.get(i) < search1.get(j)) {
                j--;
            } else {
                return search.get(i);
            }
        }

        return -1;
    }

    private static class DictTree {
        private DictTree[] children;
        private List<Integer> contains;

        public DictTree() {
            children = new DictTree[26];
            contains = new ArrayList<>();
        }

        public void add(String word, int i, boolean flip) {
            DictTree cur = this;
            if (flip) {
                for (char c : word.toCharArray()) {
                    int index = c - 'a';
                    if (cur.children[index] == null) {
                        cur.children[index] = new DictTree();
                    }
                    cur.contains.add(i);
                    cur = cur.children[index];
                }
            } else {
                char[] charArray = word.toCharArray();
                for (int j = charArray.length - 1; j >= 0; j--) {
                    char c = charArray[j];
                    int index = c - 'a';
                    if (cur.children[index] == null) {
                        cur.children[index] = new DictTree();
                    }
                    cur.contains.add(i);
                    cur = cur.children[index];
                }
            }
            cur.contains.add(i);
        }

        public List<Integer> search(char[] word) {
            DictTree cur = this;
            for (char c : word) {
                int index = c - 'a';
                if (cur.children[index] == null) {
                    return new ArrayList<>();
                }
                cur = cur.children[index];
            }
            return cur.contains;
        }
    }
}

/**
 * Your WordFilter object will be instantiated and called as such:
 * WordFilter obj = new WordFilter(words);
 * int param_1 = obj.f(pref,suff);
 */


```

