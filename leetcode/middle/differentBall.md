## 不同颜色的乒乓球
使同一个颜色的乒乓球放一起的最小交换次数

```java
[200~package test;

import java.util.ArrayList;
import java.util.List;

public class smd {

	public static void main(String[] args) {
        check(new int[]{7,0,1,3,5,2,4,6});
    
	}
    private static int[] cint ;
    private static int count;

    public static int check(int[] boll) {
        cint = new int[boll.length];
	for (int i = 0; i < boll.length; i++) {
            cint[boll[i]] = i;
        
	}
        dfs(0, cint.length-1,boll);
        System.out.println(count);
        return count;
    
    }

    /**
     * get next
     * @param i
     * @return
     */
    public static void dfs(int i, int curr, int[] boll){

	    if (curr / 2 == 0){
            return;
        
	    }
        int ret;
	if ((boll[i] & 1) == 0) {
            ret = boll[i] + 1;
        
	} else {
            ret = boll[i] - 1;
        
	}
	if (boll[i+1] != ret){
            count ++;
            cint[boll[i+1]] ^= cint[ret];
            cint[ret] ^= cint[boll[i+1]];
            cint[boll[i+1]] ^= cint[ret];
        
	}
        dfs(i+2,curr-2,boll);
    
    }
 

}
]
```
