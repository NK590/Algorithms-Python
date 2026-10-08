# 정수론 심화 (Advanced Number Theory)

Lv1~Lv3의 정수론(소수, 소인수분해, 오일러 피, 모듈러 역원, 확장 유클리드, 중국인의 나머지 정리)을 넘어, **`10¹⁸` 크기의 수를 판정·분해하고, 합성곱과 조합을 빠르게 다루고, 대칭을 수식으로 세는** 도구들입니다. 대부분 "순진한 방법은 지수적·`√n`인데 구조를 이용해 로그·`n^(1/4)`·`n log n`으로 줄인다"는 같은 발상입니다.

## 한눈에 비교

| 개념 | 푸는 것 | 핵심 도구 | 시간 |
|---|---|---|---|
| [밀러-라빈](miller-rabin/) | `10¹⁸`~ 크기 수의 소수 판정 | 제곱 사슬과 증인, 결정적 밑 집합 | O(k log³ n) |
| [폴라드 로](pollard-rho/) | 큰 합성수의 소인수분해 | 생일 역설 + 순환 탐색(브렌트) + gcd | 기대 O(n^(1/4)) |
| [FFT / NTT](fft-ntt/) | 합성곱(다항식 곱), 큰 수 곱셈 | 1의 거듭제곱근 위의 분할 정복 | O(n log n) |
| [뫼비우스 반전](mobius-inversion/) | 서로소 쌍, gcd 합, 제곱 없는 수, 약수 합의 역변환 | μ와 `⌊n/d⌋` 블록 분해 | 체 O(n), 질의 O(√n) |
| [뤼카 정리](lucas-theorem/) | `C(n, k) mod m`, `n ≤ 10¹⁸` | p진법 자리별 곱, 쿠머, 그랜빌 + CRT | O(p + log n) |
| [번사이드 보조정리](burnside-lemma/) | 회전·대칭으로 같은 배치를 하나로 센 수 | 고정점의 평균, `k^(순환 수)` | O(\|G\|·n), 목걸이 O(d(n)) |

## 문제 신호로 고르기

| 문제의 신호 | 선택 |
|---|---|
| "`10¹²` 이상의 수가 소수인가", 질의가 많다 | [밀러-라빈](miller-rabin/) |
| "`10¹⁸` 이하의 수를 소인수분해", `φ(n)`·약수 개수 | [폴라드 로](pollard-rho/) (+ 밀러-라빈) |
| "두 수열/다항식의 곱", "합이 `s`인 쌍의 수", 아주 긴 수의 곱셈 | [FFT / NTT](fft-ntt/) |
| "`gcd`가 1인 쌍의 수", "`gcd`의 합", "제곱 없는 수" | [뫼비우스 반전](mobius-inversion/) |
| "`C(n, k) mod m`"에서 `n`이 10¹⁸이거나 `m`이 합성수 | [뤼카 정리](lucas-theorem/) |
| "회전/뒤집기로 같으면 같은 것", 목걸이·큐브 색칠 | [번사이드 보조정리](burnside-lemma/) |

## 개념 사이의 관계

- [폴라드 로](pollard-rho/)는 [밀러-라빈](miller-rabin/)을 부품으로 씁니다: "이 수가 소수인가"를 먼저 확인하고 합성수만 쪼갭니다.
- [번사이드 보조정리](burnside-lemma/)의 목걸이 공식은 [오일러 피 함수](../../lv2-intermediate/06-number-theory/euler-phi/)를 쓰고, 큰 `n`에서는 [폴라드 로](pollard-rho/)의 소인수분해가 필요합니다.
- [뫼비우스 반전](mobius-inversion/)은 `φ`를 `n = Σ_{d|n} φ(d)`의 반전으로 설명하고, 반전의 일반형은 [뤼카](lucas-theorem/)의 `p`진 구조처럼 "약수/자리별 분해"의 같은 정신입니다.
- [FFT / NTT](fft-ntt/)는 [중국인의 나머지 정리](../../lv3-advanced/02-number-theory/chinese-remainder-theorem/)로 임의 모듈러·정확한 정수 합성곱까지 확장됩니다.
- [뤼카 정리](lucas-theorem/)의 일반형(`p^e` 모듈러)은 [중국인의 나머지 정리](../../lv3-advanced/02-number-theory/chinese-remainder-theorem/)와 합쳐 임의 모듈러를 다룹니다.

## 공통 원칙

- **작은 입력에서 정의대로 계산한 값과 비교**: 이 단원의 모든 구현은 시행 나눗셈, `math.comb`, 이중 반복 합성곱, 모든 색칠 나열 같은 느린 기준과 맞춰 검증했습니다. 새 변형을 만들 때도 같은 방법으로 확인하세요.
- **전제 조건을 확인**: 소수 모듈러, `n`의 범위, 합성수 여부, NTT 소수의 위수. 전제를 어기면 조용히 틀립니다.
- **파이썬의 큰 정수를 활용**: 오버플로가 없으므로 곱셈 중간값을 걱정하지 않아도 되지만, 속도는 C++보다 느립니다. 입력 크기를 [복잡도 치트시트](../../docs/complexity-cheatsheet.md)로 가늠하세요.
- **내장 함수가 더 빠른 곳을 안다**: 큰 정수 하나의 곱셈은 파이썬 `int`가, 단일 소수 판정은 작은 수에서 체나 시행 나눗셈이 더 간단합니다.

## 읽는 순서

1. [밀러-라빈](miller-rabin/): 모듈러 거듭제곱의 구조를 이용한 판정
2. [폴라드 로](pollard-rho/): 판정에서 분해로
3. [FFT / NTT](fft-ntt/): 합성곱
4. [뫼비우스 반전](mobius-inversion/): 약수 합의 반전과 서로소 세기
5. [뤼카 정리](lucas-theorem/): 큰 이항 계수의 나머지
6. [번사이드 보조정리](burnside-lemma/): 대칭을 고려한 세기

선행: [페르마의 소정리](../../lv2-intermediate/06-number-theory/fermat-little-theorem/), [오일러 피 함수](../../lv2-intermediate/06-number-theory/euler-phi/), [조합 mod 소수](../../lv2-intermediate/06-number-theory/ncr-mod/), [확장 유클리드](../../lv3-advanced/02-number-theory/extended-euclidean-algorithm/), [중국인의 나머지 정리](../../lv3-advanced/02-number-theory/chinese-remainder-theorem/). 이후: 다항식 연산, 베를캠프-매시, min_25 체 (Lv5).
