# 탐색 기법 (Search Techniques)

"모든 경우를 하나씩 보면 `O(n²)`인 문제"를 **정렬, 단조성, 한 번의 훑기**로 `O(n log n)`이나 `O(n)`으로 줄이는 다섯 가지 기법입니다. 새로운 자료구조를 배우는 것이 아니라 배열을 **어떻게 훑을지**를 배웁니다.

## 한눈에 비교

| 개념 | 핵심 도구 | 대표 문제 | 시간 |
|---|---|---|---|
| [매개변수 탐색](parametric-search/) | 답에 대한 이분 탐색 + "가능한가?" 판정 | 랜선 자르기, 공유기 설치 | O(판정 · log 범위) |
| [모노톤 스택](monotonic-stack/) | 단조로운 스택 | 오큰수, 히스토그램의 가장 큰 직사각형 | O(n) |
| [슬라이딩 윈도우](sliding-window/) | 창 + (필요하면) 모노톤 덱 | 구간 합 최대, 창 안의 최솟값 | O(n) |
| [좌표 압축](coordinate-compression/) | 정렬 + 중복 제거 + 순위 | 큰 좌표를 작은 인덱스로 | O(n log n) |
| [스위핑](sweeping/) | 이벤트 정렬 + 상태 갱신 | 최대 겹침, 구간 합치기, 스카이라인 | O(n log n) |

## 어떤 기법을 쓸까

| 문제의 신호 | 선택 |
|---|---|
| "최댓값의 최소화", "최솟값의 최대화", "조건을 만족하는 가장 큰/작은 값" | [매개변수 탐색](parametric-search/) |
| "오른쪽(왼쪽)에서 처음으로 더 큰(작은) 값", 히스토그램, 빗물 | [모노톤 스택](monotonic-stack/) |
| 길이 `K`인 연속 구간, "합이 `S` 이상인 가장 짧은 구간", "종류가 `K`개 이하" | [슬라이딩 윈도우](sliding-window/) |
| 창 안의 최댓값·최솟값 | [슬라이딩 윈도우](sliding-window/)의 모노톤 덱 |
| 값은 10⁹ 이상인데 개수가 적다, 대소 관계만 중요 | [좌표 압축](coordinate-compression/) |
| 구간의 겹침·합치기·덮인 길이, 일정(시작/끝) 문제 | [스위핑](sweeping/) |

## 기법들의 관계

- [슬라이딩 윈도우](sliding-window/)의 최댓값 덱은 [모노톤 스택](monotonic-stack/)의 확장(앞에서도 버린다)입니다.
- [스위핑](sweeping/)은 좌표가 크면 [좌표 압축](coordinate-compression/)과 함께 씁니다. 좌표 압축은 [펜윅 트리](../../lv3-advanced/01-range-query-structures/fenwick-tree/)·[세그먼트 트리](../../lv3-advanced/01-range-query-structures/segment-tree/)의 전처리이기도 합니다.
- [매개변수 탐색](parametric-search/)의 판정 함수는 대부분 그리디이거나 위의 슬라이딩 윈도우·스위핑입니다.
- 앞의 [Lv1 투 포인터](../../lv1-elementary/04-range-techniques/two-pointers/)와 [이진 탐색](../../lv1-elementary/03-binary-search/binary-search/)이 바탕입니다.

## 읽는 순서

1. [매개변수 탐색](parametric-search/): 이진 탐색을 답의 공간으로
2. [모노톤 스택](monotonic-stack/): 스택으로 "다음 큰 값"
3. [슬라이딩 윈도우](sliding-window/): 창과 덱
4. [좌표 압축](coordinate-compression/): 큰 값을 작은 인덱스로
5. [스위핑](sweeping/): 이벤트 정렬

선행: [두 포인터](../../lv1-elementary/04-range-techniques/two-pointers/), [이진 탐색](../../lv1-elementary/03-binary-search/binary-search/), [스택](../../lv1-elementary/01-data-structures/stack/), [덱](../../lv1-elementary/01-data-structures/deque/), [우선순위 큐](../../lv1-elementary/01-data-structures/priority-queue/). 이후: [펜윅 트리](../../lv3-advanced/01-range-query-structures/fenwick-tree/), [세그먼트 트리](../../lv3-advanced/01-range-query-structures/segment-tree/), [Mo's 알고리즘](../../lv3-advanced/06-query-techniques/mos-algorithm/).
