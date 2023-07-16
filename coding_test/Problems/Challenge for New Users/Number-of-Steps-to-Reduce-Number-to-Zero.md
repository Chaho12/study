# Number of Steps to Reduce a Number to Zero

목표:

Given an integer num, return the **number of steps** to reduce it to zero.
In one step, if the **current number is even, you have to divide it by 2**, otherwise, you have to **subtract 1** from it.

뒤에서부터 생각해보자.
0이 나오기전에는 무조건 1을 먼저 빼는 경우가 발생한다.
0 : n / 2 == 0, n%2 == 0 이 마지막 s 단계
1 : n / 2 == 0, n%2 == 1 인 경우가 s-1 단계
2 : n / 2 == 1, n%2 == 0 인 경우가 s-2 단계
3 : n / 2 == 1, n%2 == 1 인 경우가 s-3
4 : n / 2 == 2, n%2 == 0 인 경우가 s-3
...

간단하게 생각하면 n/2 == 0 가 나올때까지 구하면 되는거다.
n/2 > 1 이면 짝수/홀수 구분해서 처리 하면된다.

```java
int cnt = 0;
while(num/2 != 0) {
    cnt += 1;
    if (num % 2 == 0) {
        num = num/2;
    } else {
        num = num - 1;
    }
}
return cnt += 1;
```

아... contraints를 확인 안한 실수 였다.

## 전체 코드

```java
if (num < 1) {
     return num == 1 ? 1 : 0;
} else {
    while(num/2 != 0) {
        cnt += 1;
        if (num % 2 == 0) {
            num = num/2;
        } else {
            num = num - 1;
        }
    }
    return cnt += 1;
}
```

## 비고

늘 contraints를 확인하고 예외 처리를 잘해야한다.

아래 정담이 더 빠르다.

```java
var count = 0;

      while(num > 0) {
        if(num % 2 == 0)
          num /= 2;
        else
          num -= 1;
        count++;
      }

      return count;
```

## 출처

<https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/>
