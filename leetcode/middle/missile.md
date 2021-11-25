## 导弹问题

第一发导弹可以达到任意高度,后续的必须比第一发低,这算1套导弹防御系统,

现在要发射n枚导弹,要最少布置多少套导弹系统

1 <n < 1000
```go
public static int max(int[] str) {
        List<Integer> integerList = new ArrayList<>();
        for (int i = str.length - 1; i >= 0; i--) {
            boolean needAdd = true;
            for (int i1 = 0; i1 < integerList.size(); i1++) {
                if (integerList.get(i1) < str[i]) {
                    integerList.set(i1, str[i]);
                    needAdd = false;
                    break;
                }
            }
            if (needAdd) {
                integerList.add(str[i]);
            }
        }
        return integerList.size();
    }
```
