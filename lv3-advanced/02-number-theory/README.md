# 정수론 (Number Theory)

Lv2의 모듈러 연산(역원, 오일러 정리, 페르마의 소정리)을 **소수가 아닌 모듈러**와 **여러 개의 합동식**으로 확장합니다. 두 개념은 한 쌍입니다: 확장 유클리드 호제법이 계수를 구하는 도구이고, 중국인의 나머지 정리가 그 도구로 식을 합치는 응용입니다.

## 한눈에 비교

| 개념 | 푸는 것 | 핵심 조건 | 시간 |
|---|---|---|---|
| [확장 유클리드 호제법](extended-euclidean-algorithm/) | `ax + by = gcd(a, b)`, 일차 부정 방정식, 합동식 `ax ≡ b (mod m)`, 합성수 모듈러의 역원 | 해가 있을 조건은 `gcd(a, b) \| c` | O(log min(a, b)) |
| [중국인의 나머지 정리](chinese-remainder-theorem/) | 연립합동식 `x ≡ rᵢ (mod mᵢ)` | 모듈러가 서로소이면 항상 해가 있고, 아니면 `rᵢ ≡ rⱼ (mod gcd(mᵢ, mⱼ))`일 때만 | 식 하나당 O(log m) |

## 어떤 방법을 쓸까

| 상황 | 선택 |
|---|---|
| 모듈러가 소수이고 역원만 필요 | `pow(a, p − 2, p)` ([페르마](../../lv2-intermediate/06-number-theory/fermat-little-theorem/)) 또는 `pow(a, -1, p)` |
| 모듈러가 합성수이고 역원이 필요 | `pow(a, -1, m)` 또는 [확장 유클리드](extended-euclidean-algorithm/) (`gcd = 1`일 때만 존재) |
| `ax + by = c`의 정수 해 | [확장 유클리드](extended-euclidean-algorithm/): `gcd(a, b) \| c`이면 해 하나를 구하고 일반해로 범위 조정 |
| `ax ≡ b (mod m)` | `g = gcd(a, m)`로 나눠 역원을 곱한다 (해는 `mod m/g`에서 하나) |
| 두 개 이상의 합동식을 하나로 | [중국인의 나머지 정리](chinese-remainder-theorem/): 앞에서부터 두 식씩 합친다 |
| 큰 정수를 여러 소수 모듈러의 결과로 복원 | [Garner 알고리즘](chinese-remainder-theorem/) |
| 합성수 `m`에 대한 조합·거듭제곱 | `m`을 소수 거듭제곱으로 쪼개 각각 계산하고 CRT로 합치기 |

## 주의할 점

- 이 단계의 모든 알고리즘은 **`gcd`를 먼저 계산**하고 그 값이 문제의 조건에 맞는지 확인하는 것으로 시작합니다. 해가 없는 경우를 놓치지 마세요.
- 파이썬의 `%`와 `//`는 음수에서 항상 0 이상의 나머지와 내림 나눗셈을 줍니다. C++/Java로 옮길 때는 음수 처리를 따로 하세요.
- 계수와 `lcm`이 커져 `64비트`를 넘기 쉽습니다.

## 읽는 순서

1. [확장 유클리드 호제법](extended-euclidean-algorithm/): 베주 계수와 세 가지 응용
2. [중국인의 나머지 정리](chinese-remainder-theorem/): 합동식 합치기

선행: [유클리드 호제법](../../lv1-elementary/06-number-theory/euclidean-algorithm/), [모듈러 역원](../../lv2-intermediate/06-number-theory/modular-inverse/), [오일러 피 함수](../../lv2-intermediate/06-number-theory/euler-phi/). 이후: [밀러-라빈](../../lv4-expert/01-number-theory/miller-rabin/).
