## 钥匙和房间

有 N 个房间，开始时你位于 0 号房间。每个房间有不同的号码：0，1，2，...，N-1，并且房间里可能有一些钥匙能使你进入下一个房间。

在形式上，对于每个房间 i 都有一个钥匙列表 rooms[i]，每个钥匙 rooms[i][j] 由 [0,1，...，N-1] 中的一个整数表示，其中 N = rooms.length。 钥匙 rooms[i][j] = v 可以打开编号为 v 的房间。

最初，除 0 号房间外的其余所有房间都被锁住。

你可以自由地在房间之间来回走动。

如果能进入每个房间返回 true，否则返回 false。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/keys-and-rooms
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

```go
//暴力破解法无敌
func canVisitAllRooms(rooms [][]int) bool {

	keys := getKeys(0, rooms, map[int]int{})

	leng :=len(rooms)

	results := 0
	for _,val := range keys{
		results+=val
	}
	roomsum := leng*(leng -1)/2

	return results == roomsum
}


func getKeys(key int, rooms [][]int, maps map[int]int)[]int{
	keys := rooms[key]
	var roomid []int
	if keys ==  nil{
		return roomid
	}
	for _,val:= range keys{

		if maps[val]  == 0 {
			if(val == 0){
				maps[val] =1
			}else {
				maps[val] =val
			}

			ints := getKeys(val, rooms, maps)
			for _, v := range ints {
				maps[v] =v
			}
		}
	}

	for k, _ := range maps {
		roomid	= append(roomid,k)
	}

	return  roomid
}

//DFS

var (
    num int
    vis []bool
)

func canVisitAllRooms(rooms [][]int) bool {
    n := len(rooms)
    num = 0
    vis = make([]bool, n)
    dfs(rooms, 0)
    return num == n
}

func dfs(rooms [][]int, x int) {
    vis[x] = true
    num++
    for _, it := range rooms[x] {
        if !vis[it] {
            dfs(rooms, it)
        }
    }
}



```
