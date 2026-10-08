# 분할 정복 (Divide and Conquer)

문제를 **작은 문제로 쪼개 풀고 합치는** 방식을 다룹니다. 병합 정렬·퀵 정렬·이분 탐색이 모두 분할 정복이고, 빠른 거듭제곱은 "한쪽만 푸는" 가장 단순한 형태입니다.

## 한눈에 비교

| 개념 | 나누는 방식 | 합치는 단계 | 시간 |
|---|---|---|---|
| [분할 정복](divide-and-conquer/) | 반으로(또는 4등분·9등분), 양쪽 모두 푼다 | 가운데를 걸치는 경우 / 병합 / 띠 검사 | 보통 O(n log n) |
| [빠른 거듭제곱](fast-exponentiation/) | 지수를 반으로, **한쪽만** 푼다 | 제곱 (홀수면 한 번 더 곱) | O(log b) |

## 분할 정복인가 판단하는 질문

1. 입력을 **같은 모양의 더 작은 입력**으로 나눌 수 있는가? (반으로, 사분면으로)
2. 작은 문제의 답을 **합쳐서** 원래 답을 만들 수 있는가? 합치는 비용은?
3. **합치는 비용 f(n)**이 `O(n)`이면 반으로 나눌 때 `O(n log n)`, `O(1)`이면 `O(n)`, 한쪽만 풀면 `O(log n)`이다.

## 분할 정복과 다른 기법의 경계

| 상황 | 선택 |
|---|---|
| 작은 문제가 **서로 독립**이고 겹치지 않는다 | 분할 정복 |
| 작은 문제가 **겹친다** (같은 부분 문제 반복) | [DP](../04-dynamic-programming/) (메모이제이션) |
| 한 번의 선택이 이후를 망치지 않는다는 증명이 있다 | [그리디](../../lv1-elementary/07-algorithm-paradigms/greedy/) |
| 문제가 1씩만 줄어든다 (`T(n) = 2T(n−1)`) | 지수 시간. 하노이처럼 출력이 지수인 경우만 가능 |

## 읽는 순서

1. [분할 정복](divide-and-conquer/): 합치는 단계가 핵심인 예 여섯 가지
2. [빠른 거듭제곱](fast-exponentiation/): 지수를 반으로 줄이기

선행: [하노이의 탑](../../lv1-elementary/08-recursion/tower-of-hanoi/), [병합 정렬](../../lv1-elementary/02-sorting/merge-sort/). 이후: [페르마의 소정리](../06-number-theory/fermat-little-theorem/), [행렬 거듭제곱](../../lv3-advanced/07-dp-advanced/matrix-exponentiation/), [분할 정복 최적화](../../lv3-advanced/07-dp-advanced/divide-and-conquer-optimization/).
