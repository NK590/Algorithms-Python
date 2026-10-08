# 고급 DP (Advanced DP)

Lv2의 DP(배낭, LIS, 구간, 비트마스크)는 "상태를 정의하고 표를 채운다"였다면, 이 단원은 **표가 너무 커서, 점화식이 너무 느려서, 값이 확률이어서** 그대로는 안 되는 DP를 다룹니다: 상한이 10¹⁸인 수, 평균을 묻는 문제, `O(n²)`를 `O(n)`~`O(n log n)`으로 줄이는 최적화, 단계 수가 10¹⁸인 점화식.

## 한눈에 비교

| 개념 | 해결하는 어려움 | 핵심 도구 | 시간 |
|---|---|---|---|
| [자릿수 DP](digit-dp/) | 정의역이 "1~`N`의 모든 수"이고 `N`이 10¹⁸ | 높은 자리부터 + tight/free 상태 | O(자릿수 × 상태 × 진법) |
| [기댓값 DP](expected-value-dp/) | 값이 확률/평균, 순환 전이, 모듈러 출력 | `E[s] = 1 + Σ P·E[t]`, 가우스 소거, 선형성 | DAG는 O(전이), 연립방정식 O(S³) |
| [분할 정복 최적화](divide-and-conquer-optimization/) | `dp[g][i] = min_j dp[g−1][j] + cost(j, i)`의 `O(kn²)` | 최적 분할점의 단조성 + 분할 정복 | O(k n log n) |
| [볼록 껍질 트릭](convex-hull-trick/) | `dp[i] = min_j (m_j·x_i + c_j)` 꼴의 `O(n²)` | 직선들의 아래 껍질, 리차오 트리 | O(n) ~ O(n log n) |
| [행렬 거듭제곱](matrix-exponentiation/) | 선형 점화식의 `n`번째 항, `n`이 10¹⁸ | 변환 행렬 + 빠른 거듭제곱 | O(k³ log n) |

## 문제 신호로 고르기

| 문제의 신호 | 선택 |
|---|---|
| "1부터 `N`(≤10¹⁸)까지 중 자릿수 조건을 만족하는 수", 숫자 `d`의 등장 횟수 | [자릿수 DP](digit-dp/) |
| "평균 몇 번", "확률", 출력이 `p·q⁻¹ mod P` | [기댓값 DP](expected-value-dp/) |
| "연속한 `k`개 구간으로 나눠 비용 합 최소", 비용이 구간 합으로 결정 | [분할 정복 최적화](divide-and-conquer-optimization/) |
| 점화식을 전개하면 `(i의 값) × (j의 값)` 곱 항이 남는다 | [볼록 껍질 트릭](convex-hull-trick/) |
| "`n`번째 항 mod `P`"에서 `n ≤ 10¹⁸`, "길이 `L`의 경로/문자열 수" | [행렬 거듭제곱](matrix-exponentiation/) |
| 위 중 둘이 겹침 (예: 층 + 곱 항) | 층마다 CHT, 또는 분할 정복 최적화 |

## 개념 사이의 관계

- [분할 정복 최적화](divide-and-conquer-optimization/)와 [볼록 껍질 트릭](convex-hull-trick/)은 둘 다 `dp[i] = min_j dp[j] + cost(j, i)`를 가속합니다. 전자는 *층이 있는* DP의 `cost`가 monge일 때, 후자는 `cost`가 곱 항으로 *분리*될 때.
- [행렬 거듭제곱](matrix-exponentiation/)은 [빠른 거듭제곱](../../lv2-intermediate/05-divide-and-conquer/fast-exponentiation/)의 일반화이고, [아호-코라식](../05-strings-advanced/aho-corasick/)이나 [기댓값 DP](expected-value-dp/)의 전이 행렬과 결합해 단계 수가 큰 문제를 풉니다.
- [자릿수 DP](digit-dp/)도 [기댓값 DP](expected-value-dp/)처럼 "개수와 합을 함께 들고 다니는" 방식이 핵심이고, 확률을 개수 대신 쓰면 서로 연결됩니다.

## 공통 원칙

- **작은 입력의 정답부터**: 이 단원의 최적화는 모두 `O(n²)` 또는 완전 탐색과 *같은 답*이 나와야 합니다. 먼저 느린 기준 구현을 짜고 작은 입력에서 비교하세요. 각 개념의 테스트가 이 방식으로 구성되어 있습니다.
- **전제 조건을 확인**: monge, 기울기·질의의 단조성, 선형 점화식 여부. 전제가 깨지면 조용히 틀린 답이 나옵니다.
- **큰 수는 모듈러로**: 개수와 확률이 지수적으로 커지므로 문제가 요구하는 `mod`에 맞춰 중간마다 나머지를 취합니다. 파이썬은 오버플로가 없지만 *느려집니다*.

## 읽는 순서

1. [자릿수 DP](digit-dp/): 상태 압축의 기본
2. [기댓값 DP](expected-value-dp/): 확률과 평균, 모듈러
3. [분할 정복 최적화](divide-and-conquer-optimization/): 단조성으로 가속
4. [볼록 껍질 트릭](convex-hull-trick/): 직선의 아래 껍질로 가속
5. [행렬 거듭제곱](matrix-exponentiation/): 단계 수가 큰 DP

선행: [DP](../../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [비트마스크 DP](../../lv2-intermediate/04-dynamic-programming/bitmask-dp/), [구간 DP](../../lv2-intermediate/04-dynamic-programming/interval-dp/), [분할 정복](../../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/). 이후: 크누스 최적화, Aliens 트릭, 키타마사 (Lv4).
