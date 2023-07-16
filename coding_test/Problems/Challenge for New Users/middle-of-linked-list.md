# Middle of Linked List

목표

```
Given the head of a singly linked list, return the middle node of the linked list.
If there are two middle nodes, return the second middle node.
```

가장 쉽게 생각해서 풀려면 node 갯수를 count해서 그중에 절반 이후 node를 찾으면 되는 방식이지만
지난 palindrome linked list 문제에서 [Floyd's Cycle Detection Algorithm](https://en.wikipedia.org/wiki/Cycle_detection#Floyd's_tortoise_and_hare)를 배웠기 때문에 이 방식으로 한다.

알고리즘은 매우 간단하다.
2개의 head(sn, fn)를 이용해서 sn는 1개 node씩 이동, fn는 2개 node씩 이동해서 fn이 2개 이동을 못하거나 마지막 노드인 경우 sn 위치가 중앙 노드이다.

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
    public ListNode middleNode(ListNode head) {
        ListNode slowNode = head;
        ListNode fastNode = head;
        while (fastNode.next != null) {
            slowNode = slowNode.next;
            fastNode = fastNode.next.next != null ? fastNode.next.next : fastNode.next;
        }
        return slowNode;
    }
}
```

## 비고

Discussion에 찾아보니깐 ListNode 객체 선언할때 한번에 하는 방식이 더 깔끔하다.

```java
class Solution {
    public ListNode middleNode(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}
```

## 출처

<https://leetcode.com/problems/middle-of-the-linked-list/>
