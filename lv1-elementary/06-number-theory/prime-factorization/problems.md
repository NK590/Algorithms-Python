# 연습문제 — 소인수분해

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11653 소인수분해](https://www.acmicpc.net/problem/11653) | 기본형 | 소인수를 오름차순으로 출력. 1이면 아무것도 출력하지 않는다. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [백준 2312 수 복원하기](https://www.acmicpc.net/problem/2312) | 지수 | 소인수와 그 지수를 함께 출력한다 (`prime_exponents`) |
| 3 | [LeetCode 2521 Distinct Prime Factors of Product of Array](https://leetcode.com/problems/distinct-prime-factors-of-product-of-array/) | 소인수의 합집합 | 곱을 만들지 않고 각 수의 서로 다른 소인수를 `set`에 모은다 |
| 4 | [백준 1124 언더프라임](https://www.acmicpc.net/problem/1124) | 소인수의 개수 | 소인수의 개수(중복 포함)가 소수인 수를 센다. 범위의 모든 수를 분해하므로 `spf` 표가 편하다 |
| 5 | [백준 16563 어려운 소인수분해](https://www.acmicpc.net/problem/16563) | 많은 수 | 수가 많다. 체로 가장 작은 소인수 표를 만든다 (`factorize_with_spf`) |
| 6 | [백준 11689 GCD(n, k) = 1](https://www.acmicpc.net/problem/11689) | 도전 | n이 매우 크다. 서로 다른 소인수만 알면 `φ(n) = n × ∏(1 − 1/p)`. [오일러 피 함수](../../../lv2-intermediate/06-number-theory/euler-phi/)와 함께 보세요 |

## 풀이 메모

- 1~3번은 `factorize`를 그대로 씁니다. 3번은 수가 여러 개라서 값의 범위를 먼저 확인하세요.
- 4번은 분해할 수가 최대 10^5 정도로 많아 `factorize`를 반복하면 느릴 수 있습니다. 표를 한 번 만드는 비용과 비교해 보세요. ([체](../sieve-of-eratosthenes/))
- 6번은 소인수 중 **서로 다른 것**만 사용합니다. `prime_exponents`의 키를 쓰면 됩니다.
