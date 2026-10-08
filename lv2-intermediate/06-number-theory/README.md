# 정수론 (Number Theory)

"**mod 1,000,000,007**"이 붙은 문제를 푸는 도구 상자입니다. 나머지 연산에는 나눗셈이 없어서, 나눗셈을 **모듈러 역원의 곱셈**으로 바꾸는 방법을 중심으로 다룹니다. 서로 이어진 네 개념이라 순서대로 읽는 것을 권합니다.

## 한눈에 비교

| 개념 | 무엇을 하나 | 조건 | 시간 |
|---|---|---|---|
| [오일러 피 함수](euler-phi/) | `n`과 서로소인 수의 개수 `φ(n)`, 오일러 정리 `a^φ(n) ≡ 1` | `gcd(a, n) = 1` | O(√n), 표는 O(N log log N) |
| [페르마의 소정리](fermat-little-theorem/) | `a^(p−1) ≡ 1`, 역원 `a^(p−2)`, 소수 판정 | `p`가 소수 | O(log p) |
| [모듈러 역원](modular-inverse/) | 나머지 연산의 나눗셈 `a⁻¹` | `gcd(a, m) = 1` | O(log m), 표는 O(n) |
| [조합 nCr mod p](ncr-mod/) | 큰 이항 계수를 나머지로 | `p`가 소수이고 `n < p` | 전처리 O(n), 질의 O(1) |

## 어떤 방법을 쓸까

| 상황 | 선택 |
|---|---|
| `mod`가 소수(1,000,000,007, 998,244,353)이고 역원이 몇 개 필요 | `pow(a, p − 2, p)` ([페르마](fermat-little-theorem/)) |
| `mod`가 합성수이고 `gcd(a, m) = 1` | `a^(φ(m)−1)` 또는 확장 유클리드 ([오일러 피](euler-phi/), [확장 유클리드](../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/)) |
| `1..n` 모든 수의 역원이 필요 | 선형 점화식 `inv[i] = −(p // i) · inv[p % i]` |
| 조합 여러 번, `n ≤ 10⁶` | 팩토리얼·역원 팩토리얼 표 |
| 조합 한 번, `n`이 크고 `r`이 작다 | `binomial_once` (`r` 번 곱) |
| 조합인데 `mod`가 합성수 | 파스칼의 삼각형 (`n · r`이 작을 때) |
| 지수가 너무 커서 계산 불가 | 지수를 `p − 1`이나 `φ(m)`으로 줄이기 (조건 확인!) |
| 큰 수가 소수인지만 알고 싶다 | 페르마 검사는 카마이클 수에서 속는다 → [밀러-라빈](../../lv4-expert/01-number-theory/miller-rabin/) |

## 주의할 점

- `p`가 소수라는 것, `a`가 `p`의 배수가 아니라는 것, `n < p`라는 것 중 **하나라도 어긋나면** 공식이 깨집니다. 문제의 제한을 먼저 확인하세요.
- 모듈러 연산에서 `//`(정수 나눗셈)은 쓰지 않습니다. 나눗셈이 필요하면 역원을 곱합니다.
- 곱할 때마다 `% p`. 파이썬은 오버플로가 없어 틀리지는 않지만 수가 커지면 느려집니다.

## 읽는 순서

1. [오일러 피 함수](euler-phi/): 서로소의 개수와 오일러 정리
2. [페르마의 소정리](fermat-little-theorem/): 소수 모듈러에서의 역원과 지수 줄이기
3. [모듈러 역원](modular-inverse/): 방법별 비교와 역원 표
4. [조합 nCr mod p](ncr-mod/): 위의 도구를 모두 쓰는 응용

선행: [빠른 거듭제곱](../05-divide-and-conquer/fast-exponentiation/), [유클리드 호제법](../../lv1-elementary/06-number-theory/euclidean-algorithm/), [소인수분해](../../lv1-elementary/06-number-theory/prime-factorization/), [나머지 연산](../../lv0-basics/02-number-theory/modular-arithmetic/). 이후: [확장 유클리드 호제법](../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/), [중국인의 나머지 정리](../../lv3-advanced/02-number-theory/chinese-remainder-theorem/), [밀러-라빈](../../lv4-expert/01-number-theory/miller-rabin/).
