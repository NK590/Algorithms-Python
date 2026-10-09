# 연습문제 — 스프라그-그런디 정리

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [AtCoder — Stones](https://atcoder.jp/contests/dp/tasks/dp_k) | 핵심 연습 | 한 게임의 승패를 기저부터 계산한다 |
| 2 | [CSES — Nim Game I](https://cses.fi/problemset/task/1730) | 핵심 연습 | 독립한 게임을 XOR로 결합한다 |
| 3 | [CSES — Grundy's Game](https://cses.fi/problemset/task/2207) | 핵심 연습 | 서로 다른 두 더미로 분할되는 게임의 mex를 계산한다 |
| 4 | [AtCoder ABC206 F - Interval Game 2](https://atcoder.jp/contests/abc206/tasks/abc206_f) | 구간들 중 하나를 골라 그것과 겹치는 구간을 모두 없애는 게임 | 범위 `[l, r)`을 상태로 한 그런디 수 DP: 범위 안의 구간 `[a, b)`를 고르면 `[l, a)`와 `[b, r)`이 독립이라 `g(l, a) ⊕ g(b, r)`. `grundy_of`에 `(l, r)`을 위치로 |
| 5 | [AtCoder ABC278 G - Generalized Subtraction Game](https://atcoder.jp/contests/abc278/tasks/abc278_g) | 한 줄로 늘어선 돌에서 연속한 `L`~`R`개를 지우는 상호작용 게임 | 지우면 줄이 둘로 갈라지는 8진 게임과 같은 구조(`octal_game_grundy` 참고). 그런디 수 표를 만든 뒤 이기는 수 찾기 (`winning_move_in_sum`과 같은 발상) |
| 6 | [Codeforces 1091H New Year and the Tricolore Recreation](https://codeforces.com/problemset/problem/1091/H) | 소수·합성수 제약 뺄셈 게임 세 더미, `n ≤ 2·10⁵` | 그런디 수가 작다는 성질로 `mex` 후보를 비트셋으로 한꺼번에 계산 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
