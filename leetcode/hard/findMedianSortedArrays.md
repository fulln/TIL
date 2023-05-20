
## 4. Median of Two Sorted Arrays
Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return **the median** of the two sorted arrays.

The overall run time complexity should be `O(log (m+n))`.

**Example 1:**

**Input:** nums1 = [1,3], nums2 = [2]
**Output:** 2.00000
**Explanation:** merged array = [1,2,3] and median is 2.

**Example 2:**

**Input:** nums1 = [1,2], nums2 = [3,4]
**Output:** 2.50000
**Explanation:** merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

**Constraints:**

-   `nums1.length == m`
-   `nums2.length == n`
-   `0 <= m <= 1000`
-   `0 <= n <= 1000`
-   `1 <= m + n <= 2000`
-   `-106 <= nums1[i], nums2[i] <= 106`

```go
func findMedianSortedArrays(a []int, b []int) float64 {
	if len(a) > len(b) {
		a, b = b, a
	}
	m, n := len(a), len(b)
	low, high, medianPos, total := 0, len(a), (m+n+1)/2, m+n

	for low <= high  {
		cut1 := (low+high)/2;
        cut2 := medianPos - cut1;
		l1 := ternary(cut1 == 0, math.MinInt, a, cut1-1);
        l2 := ternary(cut2 == 0, math.MinInt, b, cut2-1);
        r1 := ternary(cut1 == m, math.MaxInt, a, cut1);
        r2 := ternary(cut2 == n, math.MaxInt, b, cut2);
		if l1 <= r2 && l2 <= r1 {
			if total % 2 == 1 {
				return max(l1, l2)
			} else {
				return (max(l1,l2)+min(r1,r2))/2;
			}
		} else if l1 > r2 {
			 high = cut1-1
		} else { 
			low = cut1+1
		}
	}
	return 0
}

func ternary(exp bool, a int, nums []int, idx int) int {
	if exp {
		return a
	}
	return nums[idx]
}

func min(a, b int) float64 {
	if a < b {
		return float64(a)
	}
	return float64(b)
}

func max(a, b int) float64 {
	if a > b {
		return float64(a)
	}
	return float64(b)
}

```

```java
  
public class LeetCode230520 {  
    
public double findMedianSortedArrays(int[] a, int[] b) {  
  
if (a.length > b.length) {  
return findMedianSortedArrays(b, a);  
}  
  
int n = a.length;  
int m = b.length;  
int middleTag = (n + m + 1) / 2;  
int total = m + n;  
int left = 0, right = n;  
while (left <= right) {  
int indexA = (left + right) / 2;  
int indexB = middleTag - indexA;  
int l1 = indexA == 0 ? Integer.MIN_VALUE : a[indexA - 1];  
int l2 = indexB == 0 ? Integer.MIN_VALUE : b[indexB - 1];  
int r1 = indexA == n ? Integer.MAX_VALUE : a[indexA];  
int r2 = indexB == m ? Integer.MAX_VALUE : b[indexB];  
  
if (l1 <= r2 && l2 <= r1) {  
if (total % 2 == 0) {  
return (Math.max(l1, l2) + Math.min(r1, r2)) / 2.0;  
} else {  
return Math.max(l1, l2);  
}  
} else if (l1 > r2) {  
right = indexA - 1;  
} else {  
left = indexA + 1;  
}  
}  
return 0;  
}  
  
}
```