# 연습문제 — 모듈러 역원

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 14565 역원(Inverse) 구하기](https://www.acmicpc.net/problem/14565) | 합성수의 역원 | 모듈러가 소수가 아닐 수 있고 역원이 없으면 `-1`. `gcd` 확인이 먼저. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [백준 13172 Σ](https://www.acmicpc.net/problem/13172) | 소수 모듈러 | 분수의 합을 `P · Q⁻¹ mod 1,000,000,007`로. `inverse_fermat` |
| 3 | [백준 11401 이항 계수 3](https://www.acmicpc.net/problem/11401) | 역원 팩토리얼 | `n!`, `(r!)⁻¹`, `((n−r)!)⁻¹`. [조합 nCr mod p](../ncr-mod/)로 이어진다 |
| 4 | [LeetCode 1916 Count Ways to Build Rooms in an Ant Colony](https://leetcode.com/problems/count-ways-to-build-rooms-in-an-ant-colony/) | 트리 + 역원 | 각 서브트리의 크기 곱으로 `n!`을 나누는 공식. 나눗셈 자리마다 역원을 곱하고, 크기 `1..n`의 역원을 한 번에 구하면 `inverse_table`이 쓰인다 |
| 5 | [백준 3955 캔디 분배](https://www.acmicpc.net/problem/3955) | 확장 유클리드 | 합성수 모듈러의 역원/해를 `ax + by = c`로. [확장 유클리드 호제법](../../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/)을 배운 뒤 다시 도전 |

## 풀이 메모

- 1번은 `pow(a, -1, m)`으로도 풀리지만 직접 `inverse_euler`/확장 유클리드를 구현하면서 `gcd(a, m) = 1`일 때만 존재한다는 조건을 체감해 보세요. [테스트](test_solution.py)가 작은 `(a, m)` 쌍 전부에서 `inverse_brute_force`와 비교합니다.
- 2번의 `M − 2`는 `10⁹ + 7`이 소수라서 가능합니다(`inverse_fermat`). `mod`가 소수가 아니면 `inverse_euler`를 씁니다.
- 4번은 `1..n` 전체의 역원이 필요한 경우입니다. 개수가 `10⁵`이면 `pow`를 하나씩 불러도 되지만 `10⁶`이 넘으면 [README](README.md#5-복잡도와-입력-크기-가이드)의 표처럼 차이가 커집니다.
