# 이분 탐색 (Binary Search)

**정렬된 데이터**(또는 `False…False True…True`처럼 한 번만 바뀌는 조건)에서 탐색 범위를 **절반씩 버려** 가며 O(log n)에 답을 찾는 방법입니다. n = 10^9도 약 30번이면 끝납니다.

## 한눈에 비교

| 개념 | 묻는 것 | 결과 |
|---|---|---|
| [이분 탐색](binary-search/) | 값 x가 **있는가**, 있다면 어디 | 위치 또는 −1 |
| [lower bound / upper bound](lower-upper-bound/) | x **이상(초과)이 처음 나오는** 위치 | 위치 (없으면 `len(arr)`) → 개수, 삽입 위치, floor/ceil |

## 이분 탐색이 맞는 상황

1. **배열이 정렬되어 있고** 값을 자주 찾는다 → [이분 탐색](binary-search/)
2. 같은 값이 여러 개일 때 **개수, 첫 위치, 끝 위치** → [lower/upper bound](lower-upper-bound/)
3. 배열이 없어도 "**답이 커질수록(작아질수록) 조건을 만족하기 쉬워진다**"면 답의 범위를 이분 탐색 → [매개변수 탐색](../../lv2-intermediate/08-search-techniques/parametric-search/)

## 읽는 순서

1. [이분 탐색](binary-search/): 불변식과 구간 갱신
2. [lower bound / upper bound](lower-upper-bound/): "처음 True인 위치"라는 일반적인 틀

경계 처리(`mid`를 포함할지, 올림/내림)가 가장 흔한 버그입니다. 항상 "답이 있다면 `[lo, hi]` 안에 있다"는 **불변식**을 말로 확인하며 코드를 짜세요.
