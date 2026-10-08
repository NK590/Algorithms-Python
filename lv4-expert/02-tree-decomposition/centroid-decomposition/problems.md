# 연습문제 — 센트로이드 분해

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES 2080 Fixed-Length Paths I](https://cses.fi/problemset/task/2080) | 간선 `k`개인 경로의 수 | `count_paths_with_length`와 같은 형태. 자식 조각을 하나씩 처리하며 `Counter`로 짝 찾기 |
| 2 | [Codeforces 161D Distance in Tree](https://codeforces.com/problemset/problem/161/D) | 거리가 정확히 `k`인 쌍의 수 | 1번과 같은 유형. 트리 DP(깊이별 개수)로도 풀리니 두 방법을 비교 |
| 3 | [CSES 2081 Fixed-Length Paths II](https://cses.fi/problemset/task/2081) | 간선 수가 `a` 이상 `b` 이하인 경로의 수 | "정확히" 가 아니라 *범위*. 거리별 개수의 접두사 합이나 펜윅 트리, 또는 `at_most(b) − at_most(a−1)` |
| 4 | [Codeforces 321C Ciel the Commander](https://codeforces.com/problemset/problem/321/C) | 같은 글자 사이에 더 높은 글자가 있도록 배정 | 센트로이드 트리의 깊이가 `log n ≤ 17 < 26`이라 글자 26개로 충분. 센트로이드 트리 자체를 쓰는 문제 |
| 5 | [Codeforces 342E Xenia and Tree](https://codeforces.com/problemset/problem/342/E) | 칠하기 + 가장 가까운 칠한 정점까지 거리 | [solution.py](solution.py)의 `main()`이 같은 형태. `NearestMarked`와 같은 구조 |
| 6 | [백준 5820 경주](https://www.acmicpc.net/problem/5820) | 가중치 합이 정확히 `K`인 경로 중 간선 수 최소 (IOI 2011 Race) | 센트로이드마다 "가중치 합 → 최소 간선 수" 배열을 유지, 이전 조각의 것과 합쳐 최솟값 갱신 |
| 7 | [Codeforces 914E Palindromes in a Tree](https://codeforces.com/problemset/problem/914/E) | 경로 위 글자를 재배열해 회문이 되는 경로의 수 | 글자 홀짝을 비트마스크로. 두 반쪽의 마스크가 같거나 한 비트만 다른 쌍을 센다 |
| 8 | [Codeforces 715C Digit Tree](https://codeforces.com/problemset/problem/715/C) | 경로의 숫자가 `M`으로 나누어떨어지는 순서쌍의 수 | 센트로이드로 가는 방향과 나오는 방향의 값을 따로 구하고 모듈러 역원으로 맞춘다 (`M`과 10이 서로소) |
| 9 | [Library Checker - Frequency Table of Tree Distance](https://judge.yosupo.jp/problem/frequency_table_of_tree_distance) | 모든 거리 `d`에 대해 거리가 `d`인 쌍의 수 | 센트로이드마다 깊이별 개수 배열의 **합성곱** ([FFT/NTT](../../01-number-theory/fft-ntt/)). 센트로이드 분해와 FFT의 결합 |

## 풀이 메모

- 1번과 2번은 같은 문제입니다. 센트로이드로 한 번, 트리 DP(정점의 서브트리에서 깊이별 개수 배열을 합치는 방식)로 한 번 풀어 보면 두 방법의 차이가 보입니다: DP는 `k`가 크면 배열이 커지지만 센트로이드는 `n log n`입니다.
- 3번처럼 거리 조건이 *범위* 이면, `거리가 b 이하인 쌍 − 거리가 a−1 이하인 쌍`으로 바꾸면 `count_paths_at_most`가 그대로 쓰입니다 (센트로이드마다 정렬이 들어가 `O(n log² n)`).
- 4번은 구현이 아주 짧습니다 (분해를 하고 깊이에 따라 글자를 정하면 끝). 센트로이드 트리의 성질 — 같은 깊이의 두 센트로이드 사이에는 반드시 더 얕은 센트로이드가 경로 위에 있다 — 을 그대로 쓰는 문제입니다.
- 6번은 거리가 가중치 합이라 값이 크지만 `K`가 작아서(`K ≤ 10⁶`) 배열을 쓸 수 있습니다. 센트로이드가 바뀔 때마다 배열을 *방문한 값만* 지워서 `O(조각 크기)`에 초기화하는 것이 관건입니다.
- 7번과 8번은 "두 반쪽의 합성" 이 쌍 세기의 핵심입니다. 비트마스크의 XOR, 모듈러 값의 곱과 역원이 합성입니다.
- 9번은 센트로이드 분해 + FFT를 결합하는 고급 문제입니다. 센트로이드마다 *전체* 조각의 깊이 분포를 자기 자신과 합성곱하고, *자식 조각별* 깊이 분포를 합성곱한 것을 빼는 구조입니다 (같은 "전체 − 자식별" 패턴).
