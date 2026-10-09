# 연습문제 — 센트로이드 분해

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Fixed-Length Paths I](https://cses.fi/problemset/task/2080) | 핵심 연습 | 거리별 빈도로 정확히 k인 경로 수를 센다 |
| 2 | [CSES — Fixed-Length Paths II](https://cses.fi/problemset/task/2081) | 핵심 연습 | 거리의 범위 조건으로 확장한다 |
| 3 | [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D) | 거리가 정확히 `k`인 쌍의 수 | CSES Fixed-Length Paths I과 함께, 센트로이드 분할과 깊이별 개수를 저장하는 트리 DP를 비교한다 |
| 4 | [Codeforces 321C Ciel the Commander](https://codeforces.com/problemset/problem/321/C) | 같은 글자 사이에 더 높은 글자가 있도록 배정 | 센트로이드 트리의 깊이가 `log n ≤ 17 < 26`이라 글자 26개로 충분. 센트로이드 트리 자체를 쓰는 문제 |
| 5 | [Codeforces 342E Xenia and Tree](https://codeforces.com/problemset/problem/342/E) | 칠하기 + 가장 가까운 칠한 정점까지 거리 | [solution.py](solution.py)의 `main()`이 같은 형태. `NearestMarked`와 같은 구조 |
| 6 | [Codeforces 914E Palindromes in a Tree](https://codeforces.com/problemset/problem/914/E) | 경로 위 글자를 재배열해 회문이 되는 경로의 수 | 글자 홀짝을 비트마스크로. 두 반쪽의 마스크가 같거나 한 비트만 다른 쌍을 센다 |
| 7 | [Codeforces 715C Digit Tree](https://codeforces.com/problemset/problem/715/C) | 경로의 숫자가 `M`으로 나누어떨어지는 순서쌍의 수 | 센트로이드로 가는 방향과 나오는 방향의 값을 따로 구하고 모듈러 역원으로 맞춘다 (`M`과 10이 서로소) |
| 8 | [Library Checker - Frequency Table of Tree Distance](https://judge.yosupo.jp/problem/frequency_table_of_tree_distance) | 모든 거리 `d`에 대해 거리가 `d`인 쌍의 수 | 센트로이드마다 깊이별 개수 배열의 **합성곱** ([FFT/NTT](../../01-number-theory/fft-ntt/)). 센트로이드 분해와 FFT의 결합 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
