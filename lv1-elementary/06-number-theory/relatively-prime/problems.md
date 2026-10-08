# 연습문제 — 서로소

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1735 분수 합](https://www.acmicpc.net/problem/1735) | 기약분수 | 통분한 합을 gcd로 약분한다. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 3036 링](https://www.acmicpc.net/problem/3036) | 기약분수 | 반지름의 비를 기약분수로 출력한다 |
| 3 | [LeetCode 2427 Number of Common Factors](https://leetcode.com/problems/number-of-common-factors/) | 공약수 | 공약수의 개수 = `gcd`의 약수의 개수 |
| 4 | [백준 2436 공약수](https://www.acmicpc.net/problem/2436) | 서로소 쌍 | `gcd`와 `lcm`이 주어질 때 `a = g·x`, `b = g·y`, `x`와 `y`가 서로소이고 `x·y = lcm / gcd`가 되는 쌍을 찾는다 |
| 5 | [백준 11689 GCD(n, k) = 1](https://www.acmicpc.net/problem/11689) | 도전 | n과 서로소인 k의 개수. n이 매우 커서 하나씩 세면 안 된다. [오일러 피 함수](../../../lv2-intermediate/06-number-theory/euler-phi/)를 배운 뒤 돌아오세요 |

## 풀이 메모

- 4번은 `g = gcd`, `lcm = g·x·y`임을 이용해 `x·y = lcm / g`의 약수 쌍 중 서로소이면서 합이 최소인 쌍을 찾습니다. 쌍을 고를 때 `is_coprime`을 그대로 씁니다.
- 5번은 n 이하의 수를 모두 확인하면 시간 초과입니다. n의 **서로 다른 소인수**만 알면 개수가 정해집니다. ([소인수분해](../prime-factorization/)로 소인수를 구한 뒤 φ 공식을 쓰는 문제입니다.)
