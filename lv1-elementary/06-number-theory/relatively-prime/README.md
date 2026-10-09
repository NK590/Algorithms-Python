---
level: 1
order: 2
tags: [number-theory, gcd, coprime]
prerequisites: [euclidean-algorithm]
time: O(log min(a, b))
space: O(1)
status: done
---

# Relatively Prime (서로소, Coprime)

> **한 줄 요약**: 두 수의 공약수가 1뿐이면 서로소다. `gcd(a, b) == 1`로 판정하고, 분수의 약분과 이후의 오일러 피 함수·모듈러 역원의 출발점이 된다.

## 1. 언제 쓰나 (문제 신호)

- "두 수가 **서로소**인가?", "**기약분수**로 나타내라"
- "n 이하의 수 중 n과 서로소인 수의 개수" (→ [오일러 피 함수](../../../lv2-intermediate/06-number-theory/euler-phi/)로 이어짐)
- 모듈러 연산에서 나눗셈(**모듈러 역원**)이 가능한 조건을 확인할 때
- "서로 다른 두 수를 골랐을 때 서로소인 쌍" 같은 세기 문제

## 2. 핵심 아이디어

서로소인 것은 아래 세 가지와 모두 같은 말입니다.

1. 두 수의 공약수가 **1뿐**이다.
2. **`gcd(a, b) = 1`**이다. → [유클리드 호제법](../euclidean-algorithm/)으로 O(log) 판정.
3. **`lcm(a, b) = a × b`**이다. (`gcd × lcm = a × b`이므로)

판정은 `gcd(a, b) == 1` 한 줄입니다. 1과 임의의 수는 서로소(`gcd(1, x) = 1`)이고, 서로 다른 두 소수도 서로소입니다.

**기약분수**: 분수 `n/d`의 분자와 분모를 `gcd(n, d)`로 나누면 서로소가 되어 더는 약분되지 않습니다. 합 `a/b + c/d`는 `(ad + cb) / bd`로 통분한 뒤 약분합니다.

**쌍마다 서로소 ≠ 전체의 gcd가 1**: `6, 10, 15`의 전체 gcd는 1이지만 `6`과 `10`은 서로소가 아닙니다. 문제가 "어느 두 수든 서로소"를 요구하는지, "전체가 1"을 요구하는지 구분하세요. ([solution.py](solution.py)의 `pairwise_coprime`)

### 무엇을 저장하고 어떻게 움직이나

서로소는 공통 약수가 1뿐이라는 뜻이고 두 수가 각각 소수여야 한다는 뜻은 아닙니다. 분수 약분, 주기 결합, 모듈러 역원에서 같은 조건이 나타납니다. 여러 수에서는 전체 gcd가 1인 것과 모든 쌍이 서로소인 것을 구분합니다.

### 왜 이 방법이 맞는가

분자와 분모를 gcd로 나누면 남은 둘에는 공통 인수가 없습니다. gcd가 1이면 베주 항등식으로 정수 결합해 1을 만들 수 있어 모듈러 역원도 존재합니다. 모든 수의 공약수가 없다는 조건은 각 쌍의 공약수가 없다는 조건보다 약합니다.

### 작은 예제로 검산하기

8과 9는 둘 다 합성수지만 서로소입니다. 6, 10, 15의 전체 gcd는 1이지만 각 쌍은 공약수를 가집니다. `pairwise_coprime` 같은 함수가 어느 조건을 검사하는지 이름과 계약을 확인하세요.

## 3. 손으로 따라가기

**12와 서로소인 수** (1 이상 12 이하):

| k | gcd(k, 12) | 서로소? |
|---|---|---|
| 1 | 1 | O |
| 2 | 2 | |
| 3 | 3 | |
| 4 | 4 | |
| 5 | 1 | O |
| 6 | 6 | |
| 7 | 1 | O |
| 8 | 4 | |
| 9 | 3 | |
| 10 | 2 | |
| 11 | 1 | O |
| 12 | 12 | |

결과 `[1, 5, 7, 11]`, 개수 4. 12 = 2² × 3의 소인수 2, 3의 배수가 아닌 수와 같습니다.

**분수의 합**: `2/7 + 3/5`

- 통분: `(2·5 + 3·7) / (7·5) = 31 / 35`
- `gcd(31, 35) = 1` → 이미 기약분수. **31/35**

`1/6 + 1/3`은 `(1·3 + 1·6) / 18 = 9/18`이고 `gcd(9, 18) = 9`이므로 **1/2**입니다.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def is_coprime(a, b):
    return gcd(a, b) == 1

def reduce_fraction(numerator, denominator):
    g = gcd(numerator, denominator)
    numerator, denominator = numerator // g, denominator // g
    if denominator < 0:                       # 부호는 분자에 둔다
        numerator, denominator = -numerator, -denominator
    return numerator, denominator
```

- `coprimes_up_to(limit, m)`: `m`과 서로소인 수를 모두 모읍니다. (개수를 O(√m)에 세는 방법이 오일러 피 함수입니다.)
- `add_fractions`: 두 분수의 합을 기약분수로 돌려줍니다. 직접 실행하면 두 분수를 받아 분자와 분모를 출력합니다.
- 실전에서는 `math.gcd`나 `fractions.Fraction`(자동 약분)을 쓸 수 있습니다. [테스트](test_solution.py)가 `Fraction`과 비교해 검증합니다.

## 5. 복잡도와 입력 크기 가이드

- 서로소 판정은 **O(log min(a, b))**, 공간 O(1)입니다.
- "1부터 n까지 모든 수와 서로소 판정"을 하면 O(n log n)이므로 n이 10^6 안팎이면 충분하지만, 개수만 필요하고 n이 10^12까지 커지면 소인수분해([소인수분해](../prime-factorization/)) 기반의 오일러 피 함수를 써야 합니다.

## 6. 자주 하는 실수

- **1은 소수가 아니지만 모든 수와 서로소**: `gcd(1, x) = 1`이라 코드는 자연스럽게 맞습니다. "소수 또는 1" 같은 예외 처리를 따로 넣을 필요가 없습니다.
- **`gcd(0, x)`**: `gcd(0, x) = x`라서 `x = 1`일 때만 서로소입니다. 0이 입력에 올 수 있다면 따로 따져 보세요.
- **음수 분모**: `reduce_fraction`에서 부호를 정리하지 않으면 `-1/2`와 `1/-2`가 다르게 취급됩니다.
- **분모 0**: `ZeroDivisionError`를 내서 입력 오류를 바로 드러내게 했습니다.
- **쌍 vs 전체**: 위 2절의 `6, 10, 15`를 꼭 기억하세요.

## 7. 변형과 응용

- **오일러 피 함수 φ(n)**: n 이하의 n과 서로소인 수의 개수. → [오일러 피 함수](../../../lv2-intermediate/06-number-theory/euler-phi/)
- **페르마의 소정리**: 소수 `p`와 서로소인 `a`에 대해 `a^(p−1) ≡ 1 (mod p)` → [페르마의 소정리](../../../lv2-intermediate/06-number-theory/fermat-little-theorem/)
- **모듈러 역원**: `gcd(a, m) = 1`일 때만 `a`의 역원이 존재합니다. → [확장 유클리드 호제법](../../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/)

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [유클리드 호제법](../euclidean-algorithm/)
- 이어서: [소인수분해](../prime-factorization/), [오일러 피 함수](../../../lv2-intermediate/06-number-theory/euler-phi/), [페르마의 소정리](../../../lv2-intermediate/06-number-theory/fermat-little-theorem/)
