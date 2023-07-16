# Richest Customer Wealth

목표

```
You are given an m x n integer grid accounts where accounts[i][j] is the amount of money the i​​​​​​​​​​​th​​​​ customer has in the j​​​​​​​​​​​th​​​​ bank. Return the wealth that the richest customer has.
- A customer's wealth is the amount of money they have in all their bank accounts. The richest customer is the customer that has the maximum wealth.

m == accounts.length
n == accounts[i].length
1 <= m, n <= 50
1 <= accounts[i][j] <= 100

```

간단히 생각해보면, m 계정이 있으니 모든 사람의 계정들을 전부 다 검사해야한다.
검사할때 이전 사람의 wealth를 초과하는 경우 maxWealth 값을 덮어 씌운다.

## 전체 코드

```java
class Solution {
    public int maximumWealth(int[][] accounts) {
        int curWealth = 0, maxWealth = 0;
        for (int[] m : accounts) {
            curWealth = 0;
            for (int n : m) {
                curWealth += n;
                if (maxWealth < curWealth) {
                    maxWealth = curWealth;
                }
            }
        }
        return maxWealth;
    }
}
```

## 비고

## 출처

https://leetcode.com/problems/richest-customer-wealth/
