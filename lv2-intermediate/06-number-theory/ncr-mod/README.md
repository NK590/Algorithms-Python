---
level: 2
order: 4
tags: [number-theory, combinatorics, modular, binomial]
prerequisites: [modular-inverse, fermat-little-theorem, fast-exponentiation, permutations-and-combinations]
time: 전처리 O(n), 질의 O(1)
space: O(n)
status: done
---

# nCr mod p (조합 mod 소수)

> **한 줄 요약**: `C(n, r) = n! / (r! (n−r)!)`에서 나눗셈을 **역원 곱셈**으로 바꾼다. 팩토리얼 표와 역원 팩토리얼 표를 `O(n)`에 만들어 두면 `C(n, r) mod p`가 질의마다 곱셈 두 번이다. 모듈러가 소수가 아니면 덧셈만 쓰는 파스칼의 삼각형으로 `O(n·r)`.

## 1. 언제 쓰나 (문제 신호)

- "경우의 수를 **1,000,000,007로 나눈 나머지**로 출력", 선택·배치·경로를 센다
- `C(n, r)`의 `n`이 10⁵~10⁶이고 질의가 여러 번이다
- `n`이 10⁹ 정도로 크지만 `r`이 작다 (`binomial_once`)
- **카탈란 수**(올바른 괄호, 이진 트리 개수), **격자 경로**, **중복 조합**(별과 막대)
- "서로 다른 `n`개에서 `r`개를 고른다"를 포함·배제와 섞어 쓰는 문제 (`Σ ± C(n, i) · …`)

## 2. 핵심 아이디어

**나눗셈을 곱셈으로**: `p`가 소수이고 `n < p`이면 `n!`, `r!`, `(n−r)!`은 모두 `p`와 서로소라서 역원이 있습니다.

```
C(n, r) ≡ n! · (r!)⁻¹ · ((n−r)!)⁻¹   (mod p)
```

**두 개의 표**

- `fact[i] = i! mod p` — `fact[i] = fact[i−1] · i`
- `inv_fact[i] = (i!)⁻¹ mod p`

역원을 `n`번 구하면 `O(n log p)`입니다. 대신 **마지막 하나만** `inv_fact[n] = fact[n]^(p−2)`로 구하고 거꾸로 채웁니다.

```
inv_fact[i−1] = inv_fact[i] · i       ((i−1)!⁻¹ = (i!)⁻¹ · i 이므로)
```

그러면 전처리가 `O(n + log p)`이고 질의 하나는 `fact[n] · inv_fact[r] · inv_fact[n−r]`의 곱셈 두 번입니다.

**모듈러가 합성수일 때**: 역원이 없을 수 있어서 팩토리얼 방식을 못 씁니다. 덧셈만 쓰는 **파스칼의 삼각형** `C(n, r) = C(n−1, r−1) + C(n−1, r)`로 `O(n·r)`에 구합니다. 한 줄(1차원)로 줄여 쓰면 공간이 `O(r)`입니다.

**`n ≥ p`이면 안 됩니다**: `n!`에 `p`가 인수로 들어 있어 `0`이고, 그 역원은 없습니다. 이때는 뤼카 정리를 씁니다(Lv4 예정).

## 3. 손으로 따라가기

### `p = 13`으로 `C(6, 2)` (= 15)

`n = 6 < 13`. 팩토리얼 표(`mod 13`):

| `i` | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| `fact[i]` | 1 | 1 | 2 | 6 | 24→**11** | 11·5=55→**3** | 3·6=18→**5** |

마지막 `fact[6] = 5`의 역원을 구합니다. `5 · 8 = 40 = 3 · 13 + 1`이라 `5⁻¹ = 8` (`5^11 mod 13`으로도 `8`). 이것이 `inv_fact[6] = 8`이고, 이제 거꾸로 채웁니다.

| `i` | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|---|---|---|---|---|---|---|---|
| `inv_fact[i]` | **8** | 8·6=48→**9** | 9·5=45→**6** | 6·4=24→**11** | 11·3=33→**7** | 7·2=14→**1** | 1·1→**1** |

각 칸을 `fact[i] · inv_fact[i]`로 확인하면 모두 `1 (mod 13)`입니다 (예: `fact[4] · inv_fact[4] = 11 · 6 = 66 = 5 · 13 + 1`).

```
C(6, 2) = fact[6] · inv_fact[2] · inv_fact[4] = 5 · 7 · 6
        = 35 · 6 → 9 · 6 = 54 → 54 mod 13 = 2
```

`C(6, 2) = 15 = 13 + 2`이므로 `15 mod 13 = 2`와 같습니다. 한 줄 전체 `C(6, 0..6) mod 13`은 `[1, 6, 2, 7, 2, 6, 1]`(정확한 값은 `[1, 6, 15, 20, 15, 6, 1]`)입니다.

### 파스칼로 합성수 모듈러: `mod 6`

`C(6, 2) = 15 → 15 mod 6 = 3`, `C(10, 3) = 120 → 0`. `binomial_pascal(6, 2, 6)`이 `3`, `binomial_pascal(10, 3, 6)`이 `0`을 줍니다. 역원이 필요 없고 더하기만 합니다.

### 응용 식

- **카탈란 수**: `C_n = C(2n, n) / (n+1) = C(2n, n) − C(2n, n+1)`. 뺄셈 형태를 쓰면 `(n+1)`의 역원이 필요 없습니다. `C_0..C_10 = 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796`. `C_5 = C(10, 5) − C(10, 6) = 252 − 210 = 42`.
- **격자 경로**: `rows × cols` 칸의 왼쪽 위에서 오른쪽 아래까지 오른쪽·아래로만 가는 경로는 `C(rows + cols − 2, rows − 1)`. `3 × 3`이면 `C(4, 2) = 6`. `18 × 18`이면 `C(34, 17) = 2333606220`이고 `mod 10⁹+7`은 `333606206`.
- **중복 조합(별과 막대)**: `n`종류에서 중복을 허용해 `k`개를 고르는 방법은 `C(n + k − 1, k)`. `5`종류에서 `3`개이면 `C(7, 3) = 35`.

## 4. 구현

전체 코드는 [solution.py](solution.py)에 있습니다.

```python
MOD = 1_000_000_007

def build_factorials(n, p):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % p
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], p - 2, p)         # 역원은 한 번만
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % p    # 거꾸로 채운다
    return fact, inv_fact

def binomial_mod(n, r, p, fact, inv_fact):
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % p * inv_fact[n - r] % p

def binomial_once(n, r, p=MOD):                  # 질의 하나, n 이 커도 r 이 작으면
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    numerator = denominator = 1
    for i in range(r):
        numerator = numerator * (n - i) % p
        denominator = denominator * (i + 1) % p
    return numerator * pow(denominator, p - 2, p) % p

def binomial_pascal(n, r, mod):                  # mod 가 합성수여도 됨, O(n·r)
    row = [1] + [0] * r
    for i in range(1, n + 1):
        for j in range(min(i, r), 0, -1):        # 뒤에서부터 (한 줄로 갱신)
            row[j] = (row[j] + row[j - 1]) % mod
    return row[r] % mod
```

- `catalan_mod(n, p, fact, inv_fact)`: `C(2n, n) − C(2n, n+1)`. 표는 `2n`까지 필요합니다.
- `grid_paths_mod(rows, cols, …)`, `multiset_count(n, k, …)`: 위의 응용 식.
- 직접 실행하면 `N K`를 받아 `C(N, K) mod 1,000,000,007`을 출력합니다 (`binomial_once`).
- `binomial_once(100, 50)`은 `538992043`, `binomial_once(10**9, 3)`은 `999999923`입니다.

## 5. 복잡도와 입력 크기 가이드

| 방법 | 전처리 | 질의 | 쓸 곳 |
|---|---|---|---|
| 팩토리얼 표 | O(n) | O(1) | `n ≤ 10⁶~10⁷`, 질의 여러 번 |
| `binomial_once` | 없음 | O(r + log p) | 질의 하나, `n`이 커도 `r`이 작을 때 (`n < p`) |
| 파스칼의 삼각형 | 없음 | O(n·r) | `n, r ≤ 수천`, mod가 합성수일 때 |

([복잡도 치트시트](../../../docs/complexity-cheatsheet.md)) 이 환경에서 측정한 값입니다(`p = 10⁹ + 7`, 두 번 중 최소).

| 작업 | 크기 | 시간 |
|---|---|---|
| `build_factorials` | n = 10⁶ | 0.20초 |
| `binomial_mod` 질의 | 10⁵번 (n ≤ 10⁶) | 0.08초 |
| `binomial_once` | n = 10⁶, r = 10⁵ | 0.013초 |
| `binomial_once` | n = 10⁶, r = 5·10⁵ | 0.054초 |
| `binomial_pascal` | n = 1000, r = 500 | 0.029초 |
| `binomial_pascal` | n = 2000, r = 1000 | 0.13초 |

- 파스칼은 `n·r`에 비례합니다(위 두 줄에서 `n·r`이 4배일 때 시간도 약 4.5배). 파이썬에서 `n·r ≤ 10⁷` 정도가 한계입니다.
- 질의가 많으면 표를 만들어 두고, 하나뿐이면 `binomial_once`가 표를 만드는 비용(`n`에 비례)을 아낍니다.

## 6. 자주 하는 실수

- **`n ≥ p`**: 팩토리얼에 `p`가 인수로 들어가 `0`이 되고 역원이 없어서 답이 틀립니다. `n ≤ 10⁶`에 `p = 10⁹ + 7`이면 문제없지만 `p`가 작은 소수(예: `10007`)에 `n`이 `p` 이상이면 뤼카 정리가 필요합니다.
- **모듈러가 합성수인데 팩토리얼 방식**: 역원이 없어서 틀립니다. 파스칼이나 소인수별로 계산한 뒤 [중국인의 나머지 정리](../../../lv3-advanced/02-number-theory/chinese-remainder-theorem/)로 합칩니다.
- **`r > n` 또는 `r < 0`**: `0`을 돌려줘야 하는데 인덱스 오류가 납니다. `binomial_mod`가 먼저 검사합니다.
- **표 크기**: 카탈란 수 `C_n`은 `C(2n, n)`이라 `2n`까지, 격자 경로는 `rows + cols − 2`까지 필요합니다.
- **질의마다 `pow`로 역원**: `10⁵`번이면 0.15초 정도로 버틸 만하지만 `10⁶`번이면 1.5초 이상. 역원 팩토리얼 표를 쓰세요. ([모듈러 역원](../modular-inverse/)의 측정값)
- **곱할 때 `%` 누락**: `fact[n] * inv_fact[r] * inv_fact[n-r] % p`는 파이썬에서는 맞지만 C++/Java에서는 중간 곱이 오버플로합니다. 곱셈마다 `% p`.
- **뺄셈 후 음수**: 카탈란 `C(2n, n) − C(2n, n+1)`은 파이썬의 `%`가 항상 양수를 주지만 다른 언어에서는 `+ p`를 더해야 합니다.
- **`0! = 1`**: `fact[0] = 1`이어야 `C(n, 0) = C(n, n) = 1`이 됩니다.

## 7. 변형과 응용

- **카탈란 수**: 올바른 괄호 문자열, 이진 탐색 트리의 모양 수, 볼록 다각형의 삼각분할 수.
- **별과 막대**: 중복 조합, `x₁ + … + x_k = n`의 음이 아닌 정수 해의 수 `C(n + k − 1, k − 1)`.
- **격자 경로 + 장애물**: 장애물을 좌표순으로 정렬해 "장애물을 거치는 경로를 뺀다"를 DP로 처리하고, 구간 경로 수를 `C`로 셉니다.
- **포함·배제**: `Σ (−1)^i · C(n, i) · (n − i)^k` 형태(전사 함수의 개수 등).
- **뤼카 정리**: `n ≥ p`일 때 `C(n, r) ≡ Π C(nᵢ, rᵢ) (mod p)` (`nᵢ`, `rᵢ`는 `p`진법 자리). Lv4에서 다룰 예정입니다.
- **조합의 합**: `Σ C(n, i) = 2ⁿ`, 하키 스틱 `Σ_{i=r..n} C(i, r) = C(n+1, r+1)`.

## 8. 연습문제

[problems.md](problems.md)에 쉬운 것부터 어려운 순서로 정리했습니다.

## 9. 다음 단계

- 선행: [모듈러 역원](../modular-inverse/), [페르마의 소정리](../fermat-little-theorem/), [순열과 조합](../../../lv0-basics/03-brute-force/permutations-and-combinations/)
- 이어서: [중국인의 나머지 정리](../../../lv3-advanced/02-number-theory/chinese-remainder-theorem/), [자릿수 DP](../../../lv3-advanced/07-dp-advanced/digit-dp/)
