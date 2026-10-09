# 연습문제 — 트라이

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Word Combinations](https://cses.fi/problemset/task/1731) | 핵심 연습 | 접두 트라이와 문자열 분할 DP를 결합한다 |
| 2 | [LeetCode 208 Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) | 구현 | `insert`, `search`, `startsWith`. 노드의 존재와 단어의 끝을 구분 |
| 3 | [LeetCode 14 Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) | 공통 접두사 | 트라이에서 갈라지기 전까지 내려가기 (`longest_common_prefix`) |
| 4 | [LeetCode 211 Design Add and Search Words Data Structure](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | 와일드카드 | `.`이 어떤 글자든 되는 검색. 모든 자식으로 DFS |
| 5 | [LeetCode 421 Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | 이진 트라이 | 반대 비트 우선 탐색. `max_xor_pair`와 같다 |
| 6 | [LeetCode 212 Word Search II](https://leetcode.com/problems/word-search-ii/) | 트라이 + 백트래킹 | 격자에서 사전의 단어들을 한꺼번에 찾기. 트라이로 가지치기해서 접두사가 없으면 즉시 중단 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
