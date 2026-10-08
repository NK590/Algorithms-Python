# 기타 고급 기법 (Misc)

앞 단원들에 들어가지 않지만 **고난도 문제에서 결정적인 한 수**가 되는 네 가지 기법입니다. 서로 분야가 다르고(기하, 게임 이론, 최적화, 점화식) 독립적으로 읽을 수 있습니다.

## 한눈에 비교

| 개념 | 푸는 것 | 핵심 | 시간 |
|---|---|---|---|
| [반평면 교집합](half-plane-intersection/) | 부등식 `n`개의 영역(볼록 다각형), 핵, 2차원 선형 계획 | 방향 각도 순 정렬 + 덱 | O(n log n) |
| [스프라그-그런디](sprague-grundy/) | 공정 게임의 합의 승패, 이기는 수 | 그런디 수(mex)와 XOR | 그런디 표 O(n · 수) |
| [에일리언 트릭](aliens-trick/) | "정확히 `k`개" 선택의 최적값 (볼록/오목) | 개수 대신 벌점 `λ`를 매겨 이분 탐색 | O(T · log C) |
| [키타마사](kitamasa/) | 선형 점화식의 `n`번째 항 (`n ≤ 10¹⁸`) | `xⁿ mod 특성다항식` | O(k² log n) |

## 문제 신호로 고르기

| 문제의 신호 | 선택 |
|---|---|
| `a·x + b·y ≤ c` 여러 개의 영역/넓이/존재, 다각형의 핵, 두 볼록 다각형의 교집합 | [반평면 교집합](half-plane-intersection/) |
| "볼록 다각형 안의 가장 큰 원", "최대 반지름" 같은 최적화 | [반평면 교집합](half-plane-intersection/) + 이분 탐색 |
| 두 사람이 번갈아, 마지막에 둘 수 없는 쪽이 진다, 돌 더미/구간/말이 여러 개 | [스프라그-그런디](sprague-grundy/) |
| "정확히 `k`개" 고르기, `O(nk)`가 느리다, `k`에 대해 볼록/오목 | [에일리언 트릭](aliens-trick/) |
| `a_n = c₁a_{n−1} + … + c_k a_{n−k}`, `n`이 아주 크다 | [키타마사](kitamasa/) |
| 점화식을 모른다 (수열의 앞부분만 있다) | [벌레캠프–매시](../../lv5-master/03-algebra/berlekamp-massey/) (Lv5) 후 [키타마사](kitamasa/) |

## 개념 사이의 관계

- [에일리언 트릭](aliens-trick/)과 [반평면 교집합](half-plane-intersection/)은 **볼록성**이라는 같은 뿌리를 가집니다: 에일리언 트릭은 `F(k)`가 볼록일 때 기울기(접선)로 답을 되찾고, 반평면 교집합의 결과는 볼록 다각형입니다. 에일리언 트릭 안에서 [볼록 껍질 트릭](../../lv3-advanced/07-dp-advanced/convex-hull-trick/)이 완화 DP를 `O(n)`으로 줄이는 부품이 됩니다.
- [키타마사](kitamasa/)는 Lv3의 [행렬 거듭제곱](../../lv3-advanced/07-dp-advanced/matrix-exponentiation/)을 다항식 위로 옮긴 것입니다 (`k³ → k²`). 같은 점화식을 [FFT / NTT](../01-number-theory/fft-ntt/)로 더 빠르게 만들 수도 있습니다.
- [스프라그-그런디](sprague-grundy/)는 XOR와 mex뿐인 가장 짧은 단원이지만 게임 상태를 "독립 성분의 합"으로 보는 눈이 어렵습니다. 비트 연산과 DP 표만 알면 구현은 몇 줄입니다.

## 공통 원칙

- **느린 정답과 비교**: 에일리언 트릭은 `O(nk)` DP와, 키타마사는 한 항씩 계산·행렬 거듭제곱과, 그런디는 게임 트리 전체 탐색과, 반평면 교집합은 서덜랜드-호지먼 클리핑과 무작위로 맞춰 검증했습니다.
- **정확한 산술**: 반평면 교집합은 `Fraction`, 에일리언 트릭의 동점 처리는 정수에 개수를 섞는 방식으로 오차 없이 처리합니다.
- **전제를 먼저 확인**: 볼록성(에일리언 트릭), 공정한 게임(그런디), 선형 동차 점화식(키타마사), 왼쪽이 안쪽(반평면) — 전제가 깨지면 조용히 틀립니다.

## 읽는 순서

1. [키타마사](kitamasa/): 행렬 거듭제곱의 다항식 버전 (가장 친숙)
2. [스프라그-그런디](sprague-grundy/): 게임 이론의 기본 정리
3. [반평면 교집합](half-plane-intersection/): 기하 심화
4. [에일리언 트릭](aliens-trick/): 볼록성과 이분 탐색, 앞의 도구들이 모이는 기법

선행: [행렬 거듭제곱](../../lv3-advanced/07-dp-advanced/matrix-exponentiation/), [볼록 껍질](../../lv3-advanced/04-geometry/convex-hull/), [볼록 껍질 트릭](../../lv3-advanced/07-dp-advanced/convex-hull-trick/), [매개변수 탐색](../../lv2-intermediate/08-search-techniques/parametric-search/). 이후: [벌레캠프–매시](../../lv5-master/03-algebra/berlekamp-massey/), [기울기 트릭](../../lv5-master/04-offline-dynamic/slope-trick/) (Lv5).
