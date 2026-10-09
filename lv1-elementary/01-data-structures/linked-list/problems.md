# 연습문제 — 연결 리스트

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AOJ — Doubly Linked List](https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_3_C) | 핵심 연습 | 앞뒤 연결을 바꾸며 삽입과 삭제를 수행한다 |
| 2 | [LeetCode 206 Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | 뒤집기 | `previous`, `node`로 링크 방향을 바꾼다. [solution.py](solution.py)의 `reverse` |
| 3 | [LeetCode 876 Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | 가운데 | 한 칸/두 칸 포인터를 함께 쓴다 (`middle`) |
| 4 | [LeetCode 21 Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | 합치기 | 두 리스트의 앞에서 작은 쪽을 이어 붙인다 (`merge_sorted`) |
| 5 | [LeetCode 141 Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 사이클 | 토끼와 거북이로 추가 메모리 없이 판별한다 (`has_cycle`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
