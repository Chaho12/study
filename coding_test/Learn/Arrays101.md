## Introduction

항상 예외 케이스를 생각하자.

https://leetcode.com/explore/learn/card/fun-with-arrays/521/introduction

### Squares of a Sorted Array

- Time complexity: O(n)
- space complexity: O(n)

```java
class Solution {
    public int[] sortedSquares(int[] nums) {
        int len = nums.length;
        int lp = 0;
        int rp = len-1;
        int[] res = new int[len];
        int c = 1;
        int lv = 0;
        int rv = 0;
        while (lp < rp) {
            lv = Math.abs(nums[lp]);
            rv = Math.abs(nums[rp]);
            if (lv > rv) {
                res[len-c]=lv*lv;
                c++;
                lp++;
            } else {
                res[len-c]=rv*rv;
                c++;
                rp--;
            }
        }
        res[0] = Math.abs(nums[lp]) * Math.abs(nums[rp]);
        return res;
    }
}
```


### Merge Sorted Array

- Time Complexity O(m+n)

```java
class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int lp = m-1;
        int rp = n-1;
        int lv = 0;
        int rv = 0;
        int cp = nums1.length-1;
        int negativeValue = -1000000000;
        
        while (lp >= 0 || rp >= 0) {
            lv = lp >= 0 ? nums1[lp] : negativeValue;
            rv = rp >= 0 ? nums2[rp] : negativeValue;
            
            if(lv > rv){
                nums1[cp]=lv;
                cp--;
                lp--;
            } else {
                nums1[cp]=rv;
                cp--;
                rp--;
            }
            
        }
    }
}
``````
