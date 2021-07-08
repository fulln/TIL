## 点菜展示表
给你一个数组 orders，表示客户在餐厅中完成的订单，确切地说， orders[i]=[customerNamei,tableNumberi,foodItemi] ，其中 customerNamei 是客户的姓名，tableNumberi 是客户所在餐桌的桌号，而 foodItemi 是客户点的餐品名称。

请你返回该餐厅的 点菜展示表 。在这张表中，表中第一行为标题，其第一列为餐桌桌号 “Table” ，后面每一列都是按字母顺序排列的餐品名称。接下来每一行中的项则表示每张餐桌订购的相应餐品数量，第一列应当填对应的桌号，后面依次填写下单的餐品数量。

注意：客户姓名不是点菜展示表的一部分。此外，表中的数据行应该按餐桌桌号升序排列。

 

示例 1：

输入：orders = [["David","3","Ceviche"],["Corina","10","Beef Burrito"],["David","3","Fried Chicken"],["Carla","5","Water"],["Carla","5","Ceviche"],["Rous","3","Ceviche"]]
输出：[["Table","Beef Burrito","Ceviche","Fried Chicken","Water"],["3","0","2","1","0"],["5","0","1","0","1"],["10","1","0","0","0"]] 
解释：
点菜展示表如下所示：
Table,Beef Burrito,Ceviche,Fried Chicken,Water
3    ,0           ,2      ,1            ,0
5    ,0           ,1      ,0            ,1
10   ,1           ,0      ,0            ,0
对于餐桌 3：David 点了 "Ceviche" 和 "Fried Chicken"，而 Rous 点了 "Ceviche"
而餐桌 5：Carla 点了 "Water" 和 "Ceviche"
餐桌 10：Corina 点了 "Beef Burrito" 
示例 2：

输入：orders = [["James","12","Fried Chicken"],["Ratesh","12","Fried Chicken"],["Amadeus","12","Fried Chicken"],["Adam","1","Canadian Waffles"],["Brianna","1","Canadian Waffles"]]
输出：[["Table","Canadian Waffles","Fried Chicken"],["1","2","0"],["12","0","3"]] 
解释：
对于餐桌 1：Adam 和 Brianna 都点了 "Canadian Waffles"
而餐桌 12：James, Ratesh 和 Amadeus 都点了 "Fried Chicken"

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/display-table-of-food-orders-in-a-restaurant
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go

func displayTable(orders [][]string) [][]string {
  // 从订单中获取餐品名称和桌号，统计每桌点餐数量
    nameSet := map[string]struct{}{}
    foodsCnt := map[int]map[string]int{}
    for _, order := range orders {
        id, _ := strconv.Atoi(order[1])
        food := order[2]
        nameSet[food] = struct{}{}
        if foodsCnt[id] == nil {
            foodsCnt[id] = map[string]int{}
        }
        foodsCnt[id][food]++
    }

    // 提取餐品名称，并按字母顺序排列
    n := len(nameSet)
    names := make([]string, 0, n)
    for name := range nameSet {
        names = append(names, name)
    }
    sort.Strings(names)

    // 提取桌号，并按餐桌桌号升序排列
    m := len(foodsCnt)
    ids := make([]int, 0, m)
    for id := range foodsCnt {
        ids = append(ids, id)
    }
    sort.Ints(ids)

    // 填写点菜展示表
    table := make([][]string, m+1)
    table[0] = make([]string, 1, n+1)
    table[0][0] = "Table"
    table[0] = append(table[0], names...)
    for i, id := range ids {
        cnt := foodsCnt[id]
        table[i+1] = make([]string, n+1)
        table[i+1][0] = strconv.Itoa(id)
        for j, name := range names {
            table[i+1][j+1] = strconv.Itoa(cnt[name])
        }
    }
    return table
}
```
