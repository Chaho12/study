# Roman To Integer

목표: Given a roman numeral, convert it to an integer.

```
Example 1:

Input: s = "III"
Output: 3
Explanation: III = 3.

Example 2:

Input: s = "LVIII"
Output: 58
Explanation: L = 50, V= 5, III = 3.

Example 3:

Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.
```

패턴을 보면 오른쪽에서 왼쪽으로 읽어서 계산해야지 subtraction을 계산할 수 있다.
Ex 1, ex 2는 그런 경우가 없어서 묶음 마다 더하면 되지만 예시 3번 경우 IV, XC 등 다르다.

가장 간단하게 접근한다면 오른쪽에서 왼쪽으로 읽는데, `I, V, X, L, C, D 및 M` 에서 큰게 더 높은 rank에 있다고 생각하면
낮은 rank에서 같거나 높은 rank 갈떄 새로운 묶음으로 취급하고 낮은 rank을 읽을 경우 같은 묶음으로 취급해서 계산한다.

문자 -> 값을 나타내는 Map이 하나 있어야 하고,
문자 -> rank을 의미하는 Map이 하나 있어야한다. 배열을 사용할 수도 있지만 불필요한 iteration이 생길 수 있어서 맵이 더 좋다.

```java
HashMap<Character, Integer> romanToValueMap = new HashMap<>();
map.put("I", 1);
map.put("V", 5);
map.put("X", 10);
map.put("L", 50);
map.put("C", 100);
map.put("D", 500);
map.put("M", 1000);

HashMap<Character, Integer> romanToRankMap = new HashMap<>();
map.put("I", 1);
map.put("V", 2);
map.put("X", 3);
map.put("L", 4);
map.put("C", 5);
map.put("D", 6);
map.put("M", 7);
```

그 다음에 return 값하고 비교하기 위한 char 필드 선언

```java
int sum = 0;
char previousChar = '\0';
char currentChar = previousChar;
String romanStr = "";
```

뒤에서부터 문자 하나씩 읽으면서 rank를 갖고와서 비교해나간다.

```java
for(int i = 0, n = s.length() ; i < n ; i++) {
    char c = s.charAt(n-i-1);
    if romanToRankMap.get(c) <=
}
```

## 전체 코드

```java
class Solution {
    public int romanToInt(String s) {
        HashMap<String, Integer> romanToValueMap = new HashMap<>();
        romanToValueMap.put("I", 1);
        romanToValueMap.put("IV", 4);
        romanToValueMap.put("V", 5);
        romanToValueMap.put("IX", 9);
        romanToValueMap.put("X", 10);
        romanToValueMap.put("XL", 40);
        romanToValueMap.put("L", 50);
        romanToValueMap.put("XC", 90);
        romanToValueMap.put("C", 100);
        romanToValueMap.put("CD", 400);
        romanToValueMap.put("D", 500);
        romanToValueMap.put("CM", 900);
        romanToValueMap.put("M", 1000);

        String rm = "IVXLCDM";
        HashMap<Character, Integer> romanToRankMap = new HashMap<>();
        romanToRankMap.put(rm.charAt(0), 0);
        romanToRankMap.put(rm.charAt(1), 1);
        romanToRankMap.put(rm.charAt(2), 2);
        romanToRankMap.put(rm.charAt(3), 3);
        romanToRankMap.put(rm.charAt(4), 4);
        romanToRankMap.put(rm.charAt(5), 5);
        romanToRankMap.put(rm.charAt(6), 6);

        int sum = 0;
        char previousChar = '\0';
        char currentChar = previousChar;
        String romanStr = "";
        // 낮은 rank에서 같거나 높은 rank 갈떄 새로운 묶음으로 취급하고 낮은 rank을 읽을 경우 같은 묶음으로 취급해서 계산한다.
        for(int i = 0, n = s.length() ; i < n ; i++) {
            currentChar = s.charAt(n-i-1);
            if (previousChar == '\0') { // 기존 비교할 문자가 빈 문자인 경우
                previousChar = currentChar;
                continue;
            } else if (romanToRankMap.get(currentChar) < romanToRankMap.get(previousChar)) {
                romanStr = new StringBuilder().append(currentChar).append(previousChar).toString();
                previousChar = '\0';
            } else {
                romanStr = String.valueOf(previousChar);
                previousChar = currentChar;
            }
            sum += romanToValueMap.get(romanStr);
        }
        if (previousChar != '\0') { // 만약에 마지막 끝난 문자가 빈 문자가 아닌 경우
            romanStr = String.valueOf(previousChar);
            sum += romanToValueMap.get(romanStr);
        }
        return sum;
    }
}
```

## 비고

다른 [답변](https://leetcode.com/problems/roman-to-integer/discuss/1074149/JS-Python-Java-C%2B%2B-or-Switch-Dictionary-Solution-w-Explanation-or-beats-100)을 보면 엄청 간단하게 그리고 roman 문자 특성상 문자간 값이 5배수 차이가 나는 특이점을 이용한 것을 알 수 있다.

## 문제 출처

https://leetcode.com/problems/roman-to-integer/
