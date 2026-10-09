# 연습문제 — 펜윅 트리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Point Add Range Sum](https://judge.yosupo.jp/problem/point_add_range_sum) | 핵심 연습 | 점 갱신과 반열린 구간 합을 구현한다 |
| 2 | [CSES — Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | 핵심 연습 | 질의 입력을 인덱스 규칙에 맞춰 변환한다 |
| 3 | [CSES — List Removals](https://cses.fi/problemset/task/1749) | 심화·응용 | 심화로 누적 개수에서 k번째 살아 있는 원소를 찾는다 |
| 4 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 기본형 | 점 갱신 + 구간 합. `FenwickTree.from_list`, `set`, `range_sum` |
| 5 | [LeetCode 315 Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 압축 + 개수 세기 | `count_smaller_after` |
| 6 | [LeetCode 493 Reverse Pairs](https://leetcode.com/problems/reverse-pairs/) | 변형된 역순쌍 | `a[i] > 2·a[j]`인 쌍. 압축할 때 `2·a[j]`도 함께 좌표에 포함 |
| 7 | [LeetCode 2179 Count Good Triplets in an Array](https://leetcode.com/problems/count-good-triplets-in-an-array/) | 두 순열 | 두 순열에서 모두 순서가 같은 세 쌍. 가운데 원소를 기준으로 왼쪽/오른쪽 개수를 곱한다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
