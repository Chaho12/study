# Ransom Note

목표: Given two strings ransomNote and magazine, return true if ransomNote can be constructed from magazine and false otherwise. Each letter in magazine can only be used once in ransomNote.

문자 갯수가 중요한 문제이기 때문에 HashMap 2개를 사용해서 각각 넣고
ransomNote를 iteration하면서 각 key를 magazine에서 찾아서 값을 비교

## 전체 코드

```java
class Solution {
    public boolean canConstruct(String ransomNote, String magazine) {
        HashMap<Character, Integer> rHashMap = retHashMap(ransomNote);
        HashMap<Character, Integer> mHashMap = retHashMap(magazine);

        return rHashMap.entrySet().stream().allMatch(
            entry -> mHashMap.containsKey(entry.getKey()) ? mHashMap.get(entry.getKey()) >= entry.getValue() : false
        );
    }

    private HashMap retHashMap(String s) {
        HashMap<Character, Integer> retHashMap = new HashMap<>();
        for (int i = 0, n = s.length() ; i < n ; i++) {
            retHashMap.merge(s.charAt(i), 1, Integer::sum);
        }
        return retHashMap;
    }
}
```

## 비고

## 출처

<https://leetcode.com/problems/ransom-note/>
