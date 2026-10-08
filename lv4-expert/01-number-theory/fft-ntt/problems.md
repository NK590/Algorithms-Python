# 연습문제 — FFT / NTT

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 43 Multiply Strings](https://leetcode.com/problems/multiply-strings/) | 문자열 곱셈 | 자릿수 합성곱 + 올림의 기본형. 길이가 작아 이중 반복도 되니 `multiply_decimal_strings`와 비교 |
| 2 | [백준 13277 큰 수 곱셈](https://www.acmicpc.net/problem/13277) | 십진수 곱셈 | [solution.py](solution.py)의 `main()`이 같은 형태. 자릿수 30만. 파이썬은 `int` 곱셈이 훨씬 빠르다는 것도 확인 |
| 3 | [백준 15576 FFT를 이용한 빠른 곱셈](https://www.acmicpc.net/problem/15576) | 십진수 곱셈 | 입력이 길다. 출력 올림과 앞쪽 0 |
| 4 | [백준 10531 Golf Bot](https://www.acmicpc.net/problem/10531) | 합이 가능한 값 | 지시 배열 `A`와 `A`의 합성곱 → 두 번 칠 수 있는 거리. `count_pair_sums` |
| 5 | [백준 1067 이동](https://www.acmicpc.net/problem/1067) | 원형 이동의 내적 최대 | `max_cyclic_dot_product`. 뒤집고 이어 붙이는 합성곱 |
| 6 | [Library Checker - Convolution](https://judge.yosupo.jp/problem/convolution_mod) | mod 998244353 합성곱 | `convolution(a, b)` 그대로. 입력 `5·10⁵` |
| 7 | [Library Checker - Convolution (mod 1,000,000,007)](https://judge.yosupo.jp/problem/convolution_mod_1000000007) | 임의 mod 합성곱 | 세 소수 + CRT. 정확한 범위 확인 |
| 8 | [Codeforces 993E Nikita and Order Statistics](https://codeforces.com/problemset/problem/993/E) | `k`개가 `x`보다 작은 부분 배열의 수 | 누적 합 값의 분포를 합성곱 (같은 값 쌍 세기의 변형) |
| 9 | [Codeforces 528D Fuzzy Search](https://codeforces.com/problemset/problem/528/D) | 허용 오차 있는 문자열 매칭 | 문자별 지시 배열의 합성곱 4번. 문자열 → 수열 변환 |
| 10 | [백준 11385 씀](https://www.acmicpc.net/problem/11385) | 큰 계수의 다항식 곱 | 계수가 커서 NTT 소수 하나(mod 998244353)로는 값을 담지 못한다. `convolution_exact`의 범위(`3.9·10²⁵`)를 계산해 보고 필요한 소수의 개수를 정한다 |

## 풀이 메모

- 2번과 3번은 파이썬에서 `int(a) * int(b)`로 즉시 풀립니다. NTT 구현의 정확성을 확인하는 데 쓰고(두 방법의 출력을 비교), 직접 실행해서 시간을 비교해 보세요([README](README.md#5-복잡도와-입력-크기-가이드)에 측정).
- 4번과 8번은 *합이 고정*인 쌍을 세는 합성곱의 정석입니다. 지시 배열의 길이는 값의 최댓값 + 1입니다.
- 5번은 합성곱의 인덱스 정렬이 핵심입니다. `S(s) = conv(reverse(a), b + b)[n − 1 + s]`가 되는 이유를 `n = 3`으로 손으로 확인하세요.
- 6번과 7번은 파이썬에서 `5·10⁵` 입력이 시간 제한에 걸립니다. 정확성은 작은 입력으로 검증하고, 제출은 PyPy/C++로 하는 것을 권합니다.
- 10번은 결과 계수의 크기 상한 `min(n, m) × (계수 최댓값)²`을 직접 계산해 보세요. 이 구현의 한계 `3.9·10²⁵`를 넘으면 소수를 더 써야 합니다(네 번째 소수를 추가하면 한계가 `10³⁴` 안팎으로 늘어납니다).
- 모든 문제에서 변환 길이를 `n + m − 1` 이상의 2의 거듭제곱으로 정하는 줄을 먼저 확인하세요.
