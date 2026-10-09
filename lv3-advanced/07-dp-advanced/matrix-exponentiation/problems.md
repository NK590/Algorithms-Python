# 연습문제 — 행렬 거듭제곱

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Fibonacci Numbers](https://cses.fi/problemset/task/1722) | 핵심 연습 | 피보나치 상태 전이를 행렬로 반복 적용한다 |
| 2 | [CSES — Graph Paths I](https://cses.fi/problemset/task/1723) | 핵심 연습 | 인접 행렬의 거듭제곱으로 정확히 k개 간선의 경로를 센다 |
| 3 | [CSES — Graph Paths II](https://cses.fi/problemset/task/1724) | 핵심 연습 | 합·곱 대신 min·plus 연산으로 최소 비용을 구한다 |
| 4 | [LeetCode 509 Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) | 피보나치 | `n ≤ 30`. 반복문·행렬·두 배 공식 세 방법이 모두 같은 값을 주는지 확인 |
| 5 | [LeetCode 1137 N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) | 3항 점화식 | `linear_recurrence_nth([1, 1, 1], [0, 1, 1], n)` |
| 6 | [Codeforces 450B Jzzhu and Sequences](https://codeforces.com/problemset/problem/450/B) | 2항 점화식, 음수 계수 | `fₙ = fₙ₋₁ − fₙ₋₂`. 나머지가 음수가 되지 않게. 사실 주기 6이라 행렬 없이도 풀리는 것을 알아채 보기 |
| 7 | [LeetCode 935 Knight Dialer](https://leetcode.com/problems/knight-dialer/) | 전화 키패드 위 나이트 | 10개 상태의 행렬. `n ≤ 5000`이라 단순 DP도 되니 두 방법 비교 |
| 8 | [Codeforces 691E Xor-sequences](https://codeforces.com/problemset/problem/691/E) | 조건부 이웃 그래프의 경로 수 | 두 수의 XOR의 1비트 수가 3의 배수이면 간선. `k ≤ 10¹⁸`, 정점 수 `n ≤ 100` |
| 9 | [AtCoder ABC009 D 漸化式](https://atcoder.jp/contests/abc009/tasks/abc009_4) | 다른 연산의 행렬 거듭제곱 | 곱셈이 AND, 덧셈이 XOR. 연산만 바꿔도 같은 코드가 된다는 것을 배운다 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
