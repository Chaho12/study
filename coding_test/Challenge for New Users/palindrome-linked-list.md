# Palindrome Linked List

목표 : Given the head of a singly linked list, return true if it is a palindrome.

Palindrome 인지 아닌지 확인 하기 위해서는 linked list 처음부터 끝까지 iteration 할수 밖에 없다.
`The number of nodes in the list is in the range [1, 105]` 범위가 지정되어 있으니깐
이때, 2개의 string builder를 이용해서 앞으로 더하는거와, 뒤에서 더해서 만드는 string builder를 만들고
비교하면 쉽게 답을 얻을 수 있다.

JAVA 11 에서 `System.out.println(sb1.compareTo(sb2) == 0);` 같이 비교 가능하다고 한다.

## 전체 코드

```java
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public boolean isPalindrome(ListNode head) {
        StringBuilder sbForward = new StringBuilder();
        StringBuilder sbBackward = new StringBuilder();
        ListNode curNode = head;
        while(curNode != null) {
            sbForward.append(curNode.val);
            sbBackward.insert(0, curNode.val);
            curNode = curNode.next;
        }
        return sbForward.compareTo(sbBackward) == 0;
    }
}
```

## 비고

[Floyd's Cycle Detection Algorithm](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare) 를 보면 중간값을 파악하는 로직을 이용하는데
내가 했던 방식은 가장 기본적인 방법이라 충분히 개선 여지가 있다.

- <https://leetcode.com/problems/palindrome-linked-list/discuss/1137027/JS-Python-Java-C%2B%2B-or-Easy-Floyd>'s-%2B-Reversal-Solution-w-Explanation

## 출처

<https://leetcode.com/problems/palindrome-linked-list/>
