## 行星碰撞
给定一个整数数组 asteroids，表示在同一行的行星。

对于数组中的每一个元素，其绝对值表示行星的大小，正负表示行星的移动方向（正表示向右移动，负表示向左移动）。每一颗行星以相同的速度移动。

找出碰撞后剩下的所有行星。碰撞规则：两个行星相互碰撞，较小的行星会爆炸。如果两颗行星大小相同，则两颗行星都会爆炸。两颗移动方向相同的行星，永远不会发生碰撞。

 

示例 1：

输入：asteroids = [5,10,-5]
输出：[5,10]
解释：10 和 -5 碰撞后只剩下 10 。 5 和 10 永远不会发生碰撞。
示例 2：

输入：asteroids = [8,-8]
输出：[]
解释：8 和 -8 碰撞后，两者都发生爆炸。
示例 3：

输入：asteroids = [10,2,-5]
输出：[10]
解释：2 和 -5 发生碰撞后剩下 -5 。10 和 -5 发生碰撞后剩下 10 。
示例 4：

输入：asteroids = [-2,-1,1,2]
输出：[-2,-1,1,2]
解释：-2 和 -1 向左移动，而 1 和 2 向右移动。 由于移动方向相同的行星不会发生碰撞，所以最终没有行星发生碰撞。 
 

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/asteroid-collision
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
```go
func asteroidCollision(asteroids []int) []int {
    resp := []int{asteroids[0]}
    added := true
    for i:=1;i< len(asteroids);i++{
        added = true 
                for  len(resp) > 0 &&  resp[len(resp)-1] > 0 && asteroids[i] < 0{                
                    if resp[len(resp)-1]  == asteroids[i] * -1{
                        resp = resp[:len(resp)-1]
                        added =false
                        break
                    }else if resp[len(resp)-1]  > asteroids[i] * -1{
                        added =false
                        break
                    } else{
                        resp = resp[:len(resp)-1]    
                    }
                }
                
        if added{
            resp = append(resp,asteroids[i])
        }
    }
    return resp

}
func asteroidCollision(asteroids []int) []int {
    
    ret := []int{}
    for i := 0;i < len(asteroids);{
        if len(ret) == 0{
            ret = append(ret,asteroids[i])
            i++
            continue
        }else{
            top := ret[len(ret) -1]
            if top * asteroids[i] > 0{
                ret = append(ret,asteroids[i])
                i++
            }else{
                if top < 0{
                    ret = append(ret,asteroids[i])
                    i++
                    continue
                }
                if top == -asteroids[i]{
                    ret = ret[:len(ret)-1]
                    i++
                }else if top < -asteroids[i]{
                    ret = ret[:len(ret)-1]
                }else{
                    i++
                }
            }
        }
    }
    return ret
}


```
