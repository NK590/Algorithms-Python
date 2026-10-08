# 연습문제 — 연결 리스트

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 206 Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | 뒤집기 | `previous`, `node`로 링크 방향을 바꾼다. [solution.py](solution.py)의 `reverse` |
| 2 | [LeetCode 876 Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/) | 가운데 | 한 칸/두 칸 포인터를 함께 쓴다 (`middle`) |
| 3 | [LeetCode 21 Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | 합치기 | 두 리스트의 앞에서 작은 쪽을 이어 붙인다 (`merge_sorted`) |
| 4 | [LeetCode 141 Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | 사이클 | 토끼와 거북이로 추가 메모리 없이 판별한다 (`has_cycle`) |
| 5 | [백준 1406 에디터](https://www.acmicpc.net/problem/1406) | 커서 편집 | 커서 왼쪽·오른쪽을 두 스택(또는 연결 리스트)으로 관리한다. 문자열에 직접 삽입하면 시간 초과가 난다 |
| 6 | [백준 5397 키로거](https://www.acmicpc.net/problem/5397) | 커서 편집 | 에디터와 같은 아이디어를 여러 테스트 케이스에 적용한다 |

## 풀이 메모

- 1~4번은 LeetCode의 `ListNode`가 이 저장소의 `Node`와 필드 이름(`val`/`next`)만 다릅니다. 링크를 조작하는 방식은 같습니다.
- 5, 6번은 파이썬에서 직접 연결 리스트를 만들기보다 두 스택(리스트) 방식이 훨씬 빠르고 간단합니다.
