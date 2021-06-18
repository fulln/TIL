## 按递增顺序显示卡牌
牌组中的每张卡牌都对应有一个唯一的整数。你可以按你想要的顺序对这套卡片进行排序。

最初，这些卡牌在牌组里是正面朝下的（即，未显示状态）。

现在，重复执行以下步骤，直到显示所有卡牌为止：

从牌组顶部抽一张牌，显示它，然后将其从牌组中移出。
如果牌组中仍有牌，则将下一张处于牌组顶部的牌放在牌组的底部。
如果仍有未显示的牌，那么返回步骤 1。否则，停止行动。
返回能以递增顺序显示卡牌的牌组顺序。

答案中的第一张牌被认为处于牌堆顶部。

 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/reveal-cards-in-increasing-order
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
func deckRevealedIncreasing(deck []int) []int {
	sort.Ints(deck[:]) //从小到大排序
	ret := deck[len(deck)-1:]
	deck = deck[:len(deck)-1]
	for len(deck) > 0 {
		//ret前后换
		ret = append(ret[len(ret)-1:], ret[:len(ret)-1]...)
		ret = append(deck[len(deck)-1:], ret[:]...)
		deck = deck[:len(deck)-1]
	}
	return ret
}

```