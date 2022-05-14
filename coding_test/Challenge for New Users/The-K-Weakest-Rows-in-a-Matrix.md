# The K Weakest Rows in a Matrix

목표: Return the indices of the k weakest rows in the matrix ordered from weakest to strongest.

첫번째 드는 생각은 각 row에 soldier 갯수를 count하고 나온 결과값이랑, 해당 배열 index를 갖는 객체 (oop)를 만들고 객체 ArrayList를 만든다.
하나씩 arraylist에 넣고 나서 Collections.sort 해서 weakest to strongest order 찾고
이후 K 갯수만큼 arraylist에서 get 해서 return.

## 전체 코드

```java
class Solution {
    public int[] kWeakestRows(int[][] mat, int k) {
        int ret[] = new int[k];
        int cnt = 0;
        
        List<Element> elements = new ArrayList<Element>();
        for (int i = 0; i<mat.length; i++) {
            for (int c: mat[i]) {
                if (c == 1) {
                    cnt++;
                } else {
                  break;  
                }
            }
            elements.add(new Element(i, cnt));
            cnt = 0;
        }
        Collections.sort(elements);
        for (int i = 0; i < k; i++) {
            ret[i] = elements.get(i).index;
        }
        return ret;
    }
    
   class Element implements Comparable<Element> {
        int index, value;

        Element(int index, int value){
            this.index = index;
            this.value = value;
        }

        public int compareTo(Element e) {
            return this.value - e.value;
        }
    }
}
```

## 비고

나는 OOP를 사용했지만 Priority Queue를 사용하면 훨씬 편하게 구현 할 수 있다. 애초에 넣을때부터 Sorting까지 다 되니깐 priority 기준만 명시하고 넣고 K개 읽으면 끝이다.
O(nlogn) 으로 OOP 보다 빠르다.

## 출처

<https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/>
