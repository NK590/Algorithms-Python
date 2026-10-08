# 연습문제 — 삽입 정렬

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2750 수 정렬하기](https://www.acmicpc.net/problem/2750) | 기본형 | N이 작아서 O(N²) 정렬로 풀 수 있다. 삽입 정렬을 그대로 적용해 본다 |
| 2 | [백준 10814 나이순 정렬](https://www.acmicpc.net/problem/10814) | 안정 정렬 | 나이가 같으면 먼저 가입한 사람이 앞에 와야 한다. **안정 정렬**의 성질이 문제의 핵심이다. N이 커서 삽입 정렬로는 시간 초과이니 내장 `sorted(key=...)`(안정 정렬)로 풀고, 왜 안정 정렬이어야 하는지 확인하자 |
| 3 | [LeetCode 147 Insertion Sort List](https://leetcode.com/problems/insertion-sort-list/) | 연결 리스트 | 연결 리스트에서는 원소를 밀 필요 없이 포인터만 이어 끼워 넣는다 |

## 풀이 메모

- 1번은 [solution.py](solution.py)의 `insertion_sort`로 그대로 풀립니다.
- 2번은 [selection_sort](../selection-sort/solution.py)처럼 안정적이지 않은 정렬로는 틀릴 수 있다는 점도 직접 확인해 보세요. `test_solution.py`의 안정성 검사와 같은 아이디어입니다.
