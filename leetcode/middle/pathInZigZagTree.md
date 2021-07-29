## 二叉树寻路
在一棵无限的二叉树上，每个节点都有两个子节点，树中的节点 逐行 依次按 “之” 字形进行标记。

如下图所示，在奇数行（即，第一行、第三行、第五行……）中，按从左到右的顺序进行标记；

而偶数行（即，第二行、第四行、第六行……）中，按从右到左的顺序进行标记。



给你树上某一个节点的标号 label，请你返回从根节点到该标号为 label 节点的路径，该路径是由途经的节点标号所组成的。

 

示例 1：

输入：label = 14
输出：[1,3,4,14]
示例 2：

输入：label = 26
输出：[1,2,6,10,26]
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/path-in-zigzag-labelled-binary-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func pathInZigZagTree(label int) []int {
    ret := []int{}
    count := 0;
    s :=1
    for {
        if label > s -1{
            s =  s << 1;
            count ++
        }else{
            break
        }
    }
    ret = append(ret,label)
    // 如果是偶数的话 是需要对称的点
    

    for count > 1{
        if count & 1 == 0{
            label = getReverse(label,count)/2
        }else{
            label = getReverse(label/2,count-1)   
        }
        ret = append([]int{label},ret...)
        count --
        
    }

    return ret

}

//对称的点
func getReverse(label, row int) int {
    return 1<<(row-1) + 1<<row - 1 - label
}

```
