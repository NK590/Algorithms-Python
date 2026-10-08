---
level: 2
order: 2
tags: [divide-and-conquer, math, modular]
prerequisites: [divide-and-conquer, modular-arithmetic, bitwise-operators]
time: O(log b)
space: O(1)
status: done
---

# Fast Exponentiation (빠른 거듭제곱)

> **한 줄 요약**: `a^b`를 `b`번 곱하는 대신 지수를 반으로 줄이며 제곱해 `O(log b)`번의 곱셈으로 구한다. 나머지가 붙은 `a^b mod m`은 곱할 때마다 나머지를 구해 수가 커지지 않게 한다. 지수가 10¹⁸이어도 곱셈 약 84번이면 된다.

## 1. 언제 쓰나 (문제 신호)

- "`A`를 `B`번 곱한 수를 `C`로 나눈 나머지" (B가 10⁹~10¹⁸처럼 매우 크다)
- "**1,000,000,007로 나눈 나머지를 출력**"하는 문제에서 큰 거듭제곱이 필요할 때
- 모듈러 **역원**(`a^(p−2) mod p`), 페르마의 소정리를 쓰는 조합 계산 → [페르마의 소정리](../../06-number-theory/fermat-little-theorem/)
- **점화식의 n번째 항**(피보나치, 선형 점화식)을 O(log n)에 → 행렬 거듭제곱 → [행렬 거듭제곱](../../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)
- 같은 연산을 `n`번 반복한 결과가 필요한 문제 (결합 법칙이 성립하는 모든 연산)

## 2. 핵심 아이디어

지수를 반으로 줄이는 식입니다.

```
a^b = (a^(b/2))²          (b 가 짝수)
a^b = (a^(b/2))² · a      (b 가 홀수)
a^0 = 1
```

`b`가 절반씩 줄어 `log₂ b`번 만에 0이 됩니다. [분할 정복](../divide-and-conquer/)의 "한쪽만 푼다" 형태(`T(b) = T(b/2) + O(1)`)입니다.

**반복문(이진수) 관점**: `b`를 이진수로 쓰면 켜진 비트에 해당하는 `a^(2^i)`만 곱하면 됩니다. 예를 들어 `b = 13 = 1101₂`이면 `a^13 = a^8 · a^4 · a^1`입니다. `a`를 계속 제곱하며(`a, a², a⁴, a⁸, …`) `b`의 낮은 비트부터 읽어 비트가 1이면 결과에 곱합니다.

**나머지 연산**: `(x · y) mod m = ((x mod m) · (y mod m)) mod m`이므로 **곱할 때마다** 나머지를 구해도 결과가 같습니다. 이렇게 하지 않으면 중간 값이 지수적으로 커져 수십만 자리가 됩니다.

## 3. 손으로 따라가기

### `3^13` (반복문, 낮은 비트부터)

`13 = 1101₂`. `result`는 결과, `a`는 현재의 `3^(2^i)`.

| `b` (이진수) | 낮은 비트 | `result` | `a` (다음 제곱) |
|---|---|---|---|
| 13 (`1101`) | 1 → 곱함 | 1 · 3 = 3 | 3² = 9 |
| 6 (`110`) | 0 | 3 | 9² = 81 |
| 3 (`11`) | 1 → 곱함 | 3 · 81 = 243 | 81² = 6561 |
| 1 (`1`) | 1 → 곱함 | 243 · 6561 = **1594323** | |

`3^13 = 1594323`. 12번 곱하는 대신 제곱 4번과 결과 곱 3번, 모두 7번의 곱셈입니다.

### `10^11 mod 12`

`11 = 1011₂`, 매 단계 `mod 12`.

| `b` | 낮은 비트 | `result` | `a` |
|---|---|---|---|
| 11 (`1011`) | 1 | 1 · 10 = 10 | 10² = 100 mod 12 = 4 |
| 5 (`101`) | 1 | 10 · 4 = 40 mod 12 = 4 | 4² = 16 mod 12 = 4 |
| 2 (`10`) | 0 | 4 | 4 |
| 1 (`1`) | 1 | 4 · 4 = 16 mod 12 = **4** | |

답 **4**. (`test_main`)

### 곱셈 횟수

`count_multiplications(b)` = `b`의 비트 길이(제곱) + 켜진 비트 수(결과에 곱함). 이 환경에서 확인한 값입니다.

| `b` | 1 | 2 | 10 | 13 | 1023 | 1024 | 10⁶ | 10¹⁸ |
|---|---|---|---|---|---|---|---|---|
| 곱셈 횟수 | 2 | 3 | 6 | 7 | 20 | 12 | 27 | 84 |

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
def power_mod(a, b, m):
    result = 1 % m
    a %= m
    while b > 0:
        if b & 1:                       # 지금 비트가 1 이면 결과에 곱한다
            result = result * a % m
        a = a * a % m                   # a, a², a⁴, a⁸, …
        b >>= 1
    return result

def power(a, b):                        # 재귀 버전 (나머지 없음)
    if b == 0:
        return 1
    half = power(a, b // 2)
    return half * half * a if b % 2 else half * half
```

- `power_mod_recursive`: 재귀로 쓴 같은 알고리즘. 깊이는 `log₂ b`.
- `power_float(x, n)`: 음수 지수를 허용(`x⁻ⁿ = (1/x)ⁿ`).
- `fibonacci_doubling(n)`: `(F(n), F(n+1))`을 O(log n)에. 행렬 거듭제곱을 식으로 풀어 쓴 **배가법**: `F(2k) = F(k)(2F(k+1) − F(k))`, `F(2k+1) = F(k)² + F(k+1)²`.
- `count_multiplications(b)`: 곱셈 횟수를 세어 O(log b)임을 확인합니다.
- 직접 실행하면 `A B C`를 받아 `A^B mod C`를 출력합니다.
- 파이썬에는 내장 `pow(a, b, m)`이 있습니다. 같은 알고리즘이라 실전에서는 이것을 쓰면 됩니다. ([테스트](test_solution.py)가 내장 함수와 비교합니다)

## 5. 복잡도와 입력 크기 가이드

- **시간 O(log b)** 번의 곱셈, **공간 O(1)** (반복) 또는 O(log b) (재귀). ([복잡도 치트시트](../../../docs/complexity-cheatsheet.md))
- 이 환경에서 측정한 값입니다.

| 방법 | 지수 | 시간 |
|---|---|---|
| 곱셈을 `b`번 반복 (mod 적용) | 10⁶ | 0.089초 |
| `power_mod` | 10¹⁸ | 0.000024초 |

- 지수 10⁶을 반복 곱셈으로 하면 0.09초지만, 10⁹이면 약 90초(선형 증가로 추정한 값, 측정하지 않음), 10¹⁸이면 사실상 불가능합니다.

## 6. 자주 하는 실수

- **마지막에만 `mod`**: 중간 값이 거대해져 느려지고 메모리를 씁니다. 곱할 때마다 `% m`.
- **`result = 1`이 아니라 `1 % m`**: `m = 1`이면 답은 0이어야 합니다.
- **음수 밑**: 파이썬의 `%`는 항상 `0 ≤ r < m`이라 괜찮지만 다른 언어에서는 음수가 나올 수 있습니다.
- **지수가 0**: `a^0 = 1` (a = 0이어도 보통 1로 정의). 문제의 정의를 확인하세요.
- **지수가 음수**: 정수 거듭제곱에서는 모듈러 역원이 필요합니다. → [모듈러 역원](../../06-number-theory/modular-inverse/)
- **오버플로(C++/Java)**: `m`이 10⁹ 수준이면 `a * a`가 `long long` 범위 안이지만 10¹⁸이면 `__int128`이 필요합니다. 파이썬은 문제없습니다.
- **재귀 깊이**: `log₂ b ≤ 64`라서 문제없습니다.

## 7. 변형과 응용

- **모듈러 역원**: `p`가 소수일 때 `a⁻¹ ≡ a^(p−2) (mod p)`. → [페르마의 소정리](../../06-number-theory/fermat-little-theorem/), [모듈러 역원](../../06-number-theory/modular-inverse/)
- **조합 `nCr mod p`**: 팩토리얼과 역원 팩토리얼. → [조합 nCr mod p](../../06-number-theory/ncr-mod/)
- **행렬 거듭제곱**: 숫자 대신 행렬을 곱하면 선형 점화식의 n번째 항을 O(k³ log n)에. → [행렬 거듭제곱](../../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)
- **밀러-라빈 소수 판정**: 큰 수의 소수 판정에 `a^d mod n`이 핵심. → [밀러-라빈](../../../lv4-expert/01-number-theory/miller-rabin/)
- **같은 연산의 n번 반복**: 결합 법칙만 성립하면 문자열 연결, 순열의 합성, 함수의 합성 등에도 쓸 수 있습니다.

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [분할 정복](../divide-and-conquer/), [나머지 연산](../../../lv0-basics/02-number-theory/modular-arithmetic/), [비트 연산자](../../../lv1-elementary/09-bit-manipulation/bitwise-operators/)
- 이어서: [페르마의 소정리](../../06-number-theory/fermat-little-theorem/), [모듈러 역원](../../06-number-theory/modular-inverse/), [행렬 거듭제곱](../../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)
