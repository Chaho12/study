# Fizz Buzz

목표:

```
Given an integer n, return a string array answer (1-indexed) where:
answer[i] == "FizzBuzz" if i is divisible by 3 and 5.
answer[i] == "Fizz" if i is divisible by 3.
answer[i] == "Buzz" if i is divisible by 5.
answer[i] == i (as a string) if none of the above conditions are true.
```

3의 배수는 Fizz가 들어가고, 5의 배수는 Buzz가 들어가고
공배수인 15의 배수는 FizzBuzz가 들어간다.

가장 간단하게 생각하면 배열에 값을 넣을때 3개째마다 Fizz, 5개마다 Buzz를 넣으면 된다.

## 전체 코드

```java
// runtime: 3ms, memory : 47.8 MB
class Solution {
    public List<String> fizzBuzz(int n) {
        String fizz = "Fizz";
        String buzz = "Buzz";
        String fizzbuzz = "FizzBuzz";
        List<String> answer = new ArrayList<String>();
        for(int i = 1; i <= n; i++) {
            answer.add(Integer.toString(i));
        }
        for(int i = 3; i <= n; i+=3) {
            answer.set(i-1, fizz);
        }
        for(int i = 5; i <= n; i+=5) {
            answer.set(i-1, buzz);
        }
        for(int i = 15; i <= n; i+=15) {
            answer.set(i-1, fizzbuzz);
        }
        return answer;
    }
}

// runtime: 3ms, memory : 49 MB
class Solution {
    public List<String> fizzBuzz(int n) {
        String fizz = "Fizz";
        String buzz = "Buzz";
        String fizzbuzz = "FizzBuzz";
        List<String> answer = new ArrayList<String>();
        for(int i = 1; i <= n; i++) {
            if(i % 15 == 0) {
                answer.add(fizzbuzz);
            } else if (i % 5 == 0){
                answer.add(buzz);
            } else if (i % 3 == 0){
                answer.add(fizz);
            } else {
                answer.add(Integer.toString(i));    
            }
        }
        return answer;
    }
}
```

## 비고

if 문으로 하든 for 문으로 하든 시간차이는 없고 메모리 차이만 있다.

## 출처

<https://leetcode.com/problems/fizz-buzz/>
