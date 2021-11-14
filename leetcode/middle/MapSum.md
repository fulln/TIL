#  键值映射
实现一个 MapSum 类，支持两个方法，insert 和 sum：

MapSum() 初始化 MapSum 对象
void insert(String key, int val) 插入 key-val 键值对，字符串表示键 key ，整数表示值 val 。如果键 key 已经存在，那么原来的键值对将被替代成新的键值对。
int sum(string prefix) 返回所有以该前缀 prefix 开头的键 key 的值的总和。
 

示例：

输入：
["MapSum", "insert", "sum", "insert", "sum"]
[[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
输出：
[null, null, 3, null, 5]

解释：
MapSum mapSum = new MapSum();
mapSum.insert("apple", 3);  
mapSum.sum("ap");           // return 3 (apple = 3)
mapSum.insert("app", 2);    
mapSum.sum("ap");           // return 5 (apple + app = 3 + 2 = 5)
 

提示：

1 <= key.length, prefix.length <= 50
key 和 prefix 仅由小写英文字母组成
1 <= val <= 1000
最多调用 50 次 insert 和 sum

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/map-sum-pairs
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
type MapSum struct {
    child [26]*MapSum
    isEnd bool
    va int
}


func Constructor() MapSum {
    return MapSum{}
}


func (this *MapSum) Insert(key string, val int)  {
    for _, ch := range key {
        ch -= 'a'
        if this.child[ch] == nil {
            this.child[ch] = &MapSum{}
        }
        this = this.child[ch]
    }
    this.va = val
    this.isEnd = true
}

func (this *MapSum)SearchPrefix(key string) *MapSum {
    for _, ch := range key {
        ch -= 'a'
        if this.child[ch] == nil {
            return nil
        }
        this = this.child[ch]
    }
    return this
}

func (this *MapSum)SumSingle()int{
    
    if this.isEnd {
        return this.va
    }
    sum := this.va

    for _,val := range this.child{
        if val != nil{
            fmt.Println("before",sum)
            sum += val.SumSingle()
            fmt.Println("after",sum)
        }
    }
    return sum
}


func (this *MapSum) Sum(prefix string) int {
    //前缀树
    node := this.SearchPrefix(prefix)
    return node.SumSingle()

}


/**
 * Your MapSum object will be instantiated and called as such:
 * obj := Constructor();
 * obj.Insert(key,val);
 * param_2 := obj.Sum(prefix);
 */
```
