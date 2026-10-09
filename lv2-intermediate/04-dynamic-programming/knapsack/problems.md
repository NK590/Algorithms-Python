# 연습문제 — 배낭 문제

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Book Shop](https://cses.fi/problemset/task/1158) | 핵심 연습 | 각 물건을 한 번만 쓸 때 용량을 역순으로 순회한다 |
| 2 | [AtCoder — Knapsack 1](https://atcoder.jp/contests/dp/tasks/dp_d) | 핵심 연습 | 용량을 상태로 정의한다 |
| 3 | [AtCoder — Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e) | 핵심 연습 | 가치가 작을 때 상태 축을 바꾼다 |
| 4 | [LeetCode 322 Coin Change](https://leetcode.com/problems/coin-change/) | 동전 (최소 개수) | 그리디가 틀리는 동전 체계 (`[1, 3, 4]`로 6) |
| 5 | [LeetCode 416 Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | 부분집합의 합 | 전체 합의 절반을 만들 수 있는가. `can_partition_equal` |
| 6 | [LeetCode 518 Coin Change II](https://leetcode.com/problems/coin-change-ii/) | 동전 (조합의 수) | 동전 종류를 바깥에서 순회해 순서가 다른 같은 조합을 중복으로 세지 않는다 |
| 7 | [LeetCode 494 Target Sum](https://leetcode.com/problems/target-sum/) | 부분집합 + 변환 | `+`/`-`를 붙여 합이 target. 부분집합의 합의 경우의 수로 바꾼다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
