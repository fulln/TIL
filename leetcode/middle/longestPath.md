## 2246. 相邻字符不同的最长路径

给你一棵 树（即一个连通、无向、无环图），根节点是节点 0 ，这棵树由编号从 0 到 n - 1 的 n 个节点组成。用下标从 0 开始、长度为 n 的数组 parent 来表示这棵树，其中 parent[i] 是节点 i 的父节点，由于节点 0 是根节点，所以 parent[0] == -1 。

另给你一个字符串 s ，长度也是 n ，其中 s[i] 表示分配给节点 i 的字符。

请你找出路径上任意一对相邻节点都没有分配到相同字符的 最长路径 ，并返回该路径的长度。

 

示例 1：



输入：parent = [-1,0,0,1,1,2], s = "abacbe"
输出：3
解释：任意一对相邻节点字符都不同的最长路径是：0 -> 1 -> 3 。该路径的长度是 3 ，所以返回 3 。
可以证明不存在满足上述条件且比 3 更长的路径。 
示例 2：



输入：parent = [-1,0,0,0], s = "aabc"
输出：3
解释：任意一对相邻节点字符都不同的最长路径是：2 -> 0 -> 3 。该路径的长度为 3 ，所以返回 3 。
 

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/longest-path-with-different-adjacent-characters
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```java
class Solution {
    private static char[] chars;
    private static int max;

    private Map<Integer, int[]> maps = new HashMap<>();

    public int dfs(int last, int index) {

        int[] ints = maps.get(index);

        if (ints == null) {
            if (last == -1){
                return 1;
            }else if (chars[last] == chars[index]) {
                return 0;
            } else {
                return 1;
            }
        }

        Integer[] result = new Integer[ints.length];
        for (int i= 0; i < ints.length; i++) {
            result[i] = dfs(index, ints[i]);
        }
        Arrays.sort(result, Collections.reverseOrder());

        if (result.length >= 2){
            max = Math.max(max, result[0]+ result[1] + 1);
        }else {
            max = Math.max(max, result[0] + 1);
        }


        if (last == -1) {
            return 1 + result[0];
        } else if (chars[last] == chars[index]) {
            return 0;
        } else {
            return 1 + result[0];
        }
    }


    public int longestPath(int[] parent, String s) {
        chars = s.toCharArray();
        max = 1;
        for (int i = 0; i < parent.length; i++) {
            if (maps.get(parent[i]) == null) {
                maps.put(parent[i], new int[]{i});
            } else {
                int[] ints = maps.get(parent[i]);
                int[] temp = new int[ints.length + 1];
                System.arraycopy(ints, 0, temp, 0, ints.length);
                temp[ints.length] = i;
                maps.put(parent[i], temp);
            }
        }
        dfs(-1, 0);
        return max;
    }
}
```
