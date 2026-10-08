# 연습문제 — 스프라그-그런디 정리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11868 님 게임 2](https://www.acmicpc.net/problem/11868) | 일반 님, 선공이 이기면 `koosaga` | [solution.py](solution.py)의 `main()`이 같은 형태. XOR 한 줄 |
| 2 | [백준 11694 님 게임](https://www.acmicpc.net/problem/11694) | **미제르 님** (마지막 돌을 가져가면 진다) | `misere_nim_first_player_wins`. 크기 2 이상의 더미가 있는지 먼저 확인 |
| 3 | [백준 11867 박스 나누기](https://www.acmicpc.net/problem/11867) | 상자 하나를 둘로 쪼개는 게임 | 더미가 갈라질 때 두 부분의 그런디 수를 XOR. 작은 `n`에서 표를 만들어 규칙 발견 |
| 4 | [백준 16877 핌버](https://www.acmicpc.net/problem/16877) | 피보나치 수만큼만 가져가는 뺄셈 게임 여러 더미 | `grundy_subtraction(n, 피보나치 수들)` 후 XOR. 더미 크기가 커서 수열 표를 한 번만 만들기 |
| 5 | [AtCoder ABC206 F - Interval Game 2](https://atcoder.jp/contests/abc206/tasks/abc206_f) | 구간들 중 하나를 골라 그것과 겹치는 구간을 모두 없애는 게임 | 범위 `[l, r)`을 상태로 한 그런디 수 DP: 범위 안의 구간 `[a, b)`를 고르면 `[l, a)`와 `[b, r)`이 독립이라 `g(l, a) ⊕ g(b, r)`. `grundy_of`에 `(l, r)`을 위치로 |
| 6 | [AtCoder ABC278 G - Generalized Subtraction Game](https://atcoder.jp/contests/abc278/tasks/abc278_g) | 한 줄로 늘어선 돌에서 연속한 `L`~`R`개를 지우는 상호작용 게임 | 지우면 줄이 둘로 갈라지는 8진 게임과 같은 구조(`octal_game_grundy` 참고). 그런디 수 표를 만든 뒤 이기는 수 찾기 (`winning_move_in_sum`과 같은 발상) |
| 7 | [Codeforces 1091H New Year and the Tricolore Recreation](https://codeforces.com/problemset/problem/1091/H) | 소수·합성수 제약 뺄셈 게임 세 더미, `n ≤ 2·10⁵` | 그런디 수가 작다는 성질로 `mex` 후보를 비트셋으로 한꺼번에 계산 |

## 풀이 메모

- 1번과 2번의 차이를 꼭 직접 확인하세요: 같은 입력에 일반 님은 XOR이 0인가 보고, 미제르 님은 "모든 더미가 1 이하인가" 를 먼저 봅니다. [test_solution.py](test_solution.py)의 미제르 시험은 모든 작은 상태를 게임 트리 탐색으로 확인한 결과입니다.
- 3번은 작은 `n`(1~10)의 그런디 수를 표로 만들어 규칙(홀수/짝수에 따른 값)을 찾는 연습입니다. 구현은 `grundy_of(n, 다음_위치들)`로 하고, 다음 위치에서 `(a, b)`로 쪼개진 상태는 위치를 튜플 `(a, b)`로 두어도 됩니다.
- 4번은 피보나치 수가 약 30개뿐이라 `O(n · 30)`입니다. 그런디 수가 최대 `O(log n)` 정도의 작은 값이라는 성질도 확인해 보세요.
- 5번은 구간이 쪼개지면 양쪽이 독립이라는 점이 핵심입니다. 상태가 구간 `(l, r)`이므로 `grundy_of`의 위치가 두 정수의 튜플이고, 합 규칙은 "쪼개진 구간들의 XOR".
- 6번은 상호작용 문제라 이 저장소의 `main()` 형식과 다릅니다. 그런디 수 표를 만드는 부분(`octal_game_grundy`와 같은 형태)과 이기는 수를 찾는 부분만 연습하면 됩니다.
- 7번은 이 단원에서 가장 어려운 응용입니다. 그런디 수를 모두 구하는 비용을 줄이기 위해 "각 그런디 수 값이 나타나는 위치 집합" 을 비트셋으로 관리합니다.
