# 연습문제 — 분할 정복 최적화

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Slimes](https://atcoder.jp/contests/dp/tasks/dp_n) | 선행 연습 | 선행으로 분할점 DP를 만들되 이 문제는 Knuth 최적화와의 차이도 살핀다 |
| 2 | [LeetCode 1478 Allocate Mailboxes](https://leetcode.com/problems/allocate-mailboxes/) | 우체통 `k`개의 거리 합 | `n ≤ 100`이라 `O(kn²)`로 충분하지만 비용 `중앙값 거리 합`이 monge인지 `is_monge`로 확인하는 연습 |
| 3 | [Codeforces 321E Ciel and Gondolas](https://codeforces.com/problemset/problem/321/E) | 쌍의 비용이 있는 나누기 | 비용 `cost(j, i)` = 구간 안 모든 쌍의 값. 2차원 누적 합으로 `O(1)` |
| 4 | [Codeforces 833B The Bakery](https://codeforces.com/problemset/problem/833/B) | 서로 다른 값의 수의 합 최대 | 비용 = 구간의 서로 다른 값의 수 (최대화). 비용 계산을 구간 이동으로 |
| 5 | [Codeforces 868F Yet Another Minimization Problem](https://codeforces.com/problemset/problem/868/F) | 같은 값 쌍의 수의 합 최소 | 모스 알고리즘 식으로 비용을 점진적으로 갱신하며 분할 정복 안에서 계산 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
