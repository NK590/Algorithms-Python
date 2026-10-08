# 구간 질의 자료구조 (Range Query Structures)

"배열의 구간에 대한 질문(합, 최솟값, …)"에 빠르게 답하는 자료구조입니다. 값이 **바뀌는가**, 질문이 **무엇인가**, 갱신이 **한 칸인가 구간인가**로 고릅니다.

## 한눈에 비교

| 개념 | 갱신 | 질의 | 구축 | 공간 | 질의 연산 |
|---|---|---|---|---|---|
| [누적 합](../../lv1-elementary/04-range-techniques/prefix-sum/) (Lv1) | 없음 | O(1) | O(n) | O(n) | 합 |
| [펜윅 트리](fenwick-tree/) | 점 O(log n) | O(log n) | O(n) | O(n) | 합 (역연산이 있는 연산) |
| [세그먼트 트리](segment-tree/) | 점 O(log n) | O(log n) | O(n) | O(n) | 결합 법칙을 만족하는 모든 연산 |
| [느리게 갱신되는 세그먼트 트리](lazy-propagation/) | **구간** O(log n) | O(log n) | O(n) | O(n) | 구간 갱신에 맞는 연산 |
| [희소 배열](sparse-table/) | 없음 | **O(1)** | O(n log n) | O(n log n) | 겹쳐도 되는 연산 (min, max, gcd), 분리 희소 배열은 모든 연산 |

## 어떤 것을 쓸까

| 상황 | 선택 |
|---|---|
| 값이 안 바뀌고 합만 | [누적 합](../../lv1-elementary/04-range-techniques/prefix-sum/) |
| 값이 안 바뀌고 최솟값·최댓값·gcd | [희소 배열](sparse-table/) |
| 한 칸 바뀌고 합 | [펜윅 트리](fenwick-tree/) (가장 짧고 빠름) |
| 한 칸 바뀌고 최솟값·최댓값·gcd·곱 | [세그먼트 트리](segment-tree/) |
| 구간 전체에 더하기, 합 | [펜윅 트리의 `RangeAddFenwick`](fenwick-tree/) (가볍다) 또는 [느리게 갱신되는 세그먼트 트리](lazy-propagation/) |
| 구간 대입, 구간 뒤집기, 구간 더하기 + 최솟값 | [느리게 갱신되는 세그먼트 트리](lazy-propagation/) |
| 구간마다 여러 값(최대 연속 부분 합, 개수)을 함께 | [세그먼트 트리](segment-tree/)의 튜플 노드 |
| 역순쌍, "뒤에 있는 더 작은 수의 개수" | [펜윅 트리](fenwick-tree/) + [좌표 압축](../../lv2-intermediate/08-search-techniques/coordinate-compression/) |
| 동적 집합의 `k`번째 수 | [펜윅 트리의 `find_kth`](fenwick-tree/) 또는 [세그먼트 트리](segment-tree/) 내려가기 |

## 파이썬에서의 속도

모두 이 환경에서 측정한 값입니다 (자세한 표는 각 문서).

- 질의 `10⁵`개 기준으로 세그먼트 트리(반복문)는 약 0.3초, 같은 알고리즘의 재귀 구현은 약 1.0초입니다. **아래에서 위로 올라가는 반복문 구현**을 우선하세요.
- 합 문제는 펜윅 트리가 세그먼트 트리보다 약 2배 빠릅니다.
- 재귀 구현의 느리게 갱신되는 세그먼트 트리는 구간 갱신·질의 5만 쌍에 2초 정도라, 구간 더하기·구간 합이라면 `RangeAddFenwick`(0.45초)을 먼저 고려하세요.
- 정적 배열이면 희소 배열의 질의가 세그먼트 트리보다 약 8배 빠릅니다.

## 읽는 순서

1. [펜윅 트리](fenwick-tree/): 가장 단순한 형태, 접두사 합
2. [세그먼트 트리](segment-tree/): 일반 연산과 비가환 결합
3. [느리게 갱신되는 세그먼트 트리](lazy-propagation/): 구간 갱신
4. [희소 배열](sparse-table/): 정적 배열의 `O(1)` 질의

선행: [누적 합](../../lv1-elementary/04-range-techniques/prefix-sum/), [트리](../../lv1-elementary/05-graph-basics/tree/), [분할 정복](../../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/), [좌표 압축](../../lv2-intermediate/08-search-techniques/coordinate-compression/). 이후: [최소 공통 조상](../03-graph-advanced/lca/), [Mo's 알고리즘](../06-query-techniques/mos-algorithm/), [제곱근 분할](../06-query-techniques/sqrt-decomposition/).
