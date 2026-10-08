# 연습문제 — 트립

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [SPOJ ORDERSET - Order statistic set](https://www.spoj.com/problems/ORDERSET/) | 삽입·삭제·`k`번째·순위 | `OrderedMultiset`의 기본 연산. 중복을 허용하지 않는 집합이므로 `count`로 먼저 확인하고 넣는다 |
| 2 | [백준 7662 이중 우선순위 큐](https://www.acmicpc.net/problem/7662) | 최솟값·최댓값을 모두 꺼내는 큐 | `pop_min`/`pop_max`. 두 개의 힙 + 지연 삭제로도 풀리니 비교 |
| 3 | [백준 1572 중앙값](https://www.acmicpc.net/problem/1572) | 슬라이딩 윈도우 중앙값의 합 | 윈도우가 움직일 때 `add`/`remove`, 중앙값은 `kth_smallest`. 값 범위가 작으니 펜윅 트리로도 풀린다 |
| 4 | [Library Checker - Range Reverse Range Sum](https://judge.yosupo.jp/problem/range_reverse_range_sum) | 구간 뒤집기 + 구간 합 | [solution.py](solution.py)의 `main()`이 같은 형태. 암시적 트립의 기본 |
| 5 | [Codeforces 863D Yet Another Array Queries Problem](https://codeforces.com/problemset/problem/863/D) | 구간 순환 이동·뒤집기 후 몇 개 위치의 값 | 순환 이동은 `move`(잘라 붙이기)로. 질의 수가 적으면 거꾸로 위치를 추적하는 `O(q)` 풀이도 있다 |
| 6 | [Library Checker - Dynamic Sequence Range Affine Range Sum](https://judge.yosupo.jp/problem/dynamic_sequence_range_affine_range_sum) | 삽입·삭제 + 구간 뒤집기 + 구간 아핀 변환 + 구간 합 | 지연 태그가 `x → a·x + b`로 바뀐다. 태그 합성 순서와 `total`에 합성하는 규칙을 직접 유도해야 한다 |
| 7 | [Codeforces 702F T-Shirts](https://codeforces.com/problemset/problem/702/F) | 사람마다 가진 돈 안에서 티셔츠를 사는 시뮬레이션 | 값(남은 돈)을 키로 하는 트립에 구간 빼기 태그. 값이 변한 뒤 순서가 어긋나는 부분을 떼어 다시 삽입하는 고난도 응용 |

## 풀이 메모

- 1번~3번은 `OrderedMultiset`만 쓰는 문제입니다. 3번은 값 범위가 작아 [펜윅 트리](../../../lv3-advanced/01-range-query-structures/fenwick-tree/) 위 이분 탐색으로 `O(log n)` 중앙값을 구하는 풀이도 있어 속도를 비교해 볼 만합니다.
- 4번이 암시적 트립의 출발점입니다. `reverse(l, r)`와 `range_sum(l, r)`을 같은 트립에서 번갈아 해도 `to_list()`와 합이 순진한 리스트 연산과 같은지 [test_solution.py](test_solution.py)처럼 무작위로 비교하세요.
- 5번은 질의 수 `q ≤ 100` 정도로 작아서 트립이 필수는 아닙니다. `move`와 `reverse`로 직접 구현해 보는 연습으로 좋습니다.
- 6번은 `total[t]`가 `(합, 길이)` 형태의 값이어야 아핀 태그를 `total = a·total + b·size`로 적용할 수 있습니다. 태그끼리의 합성은 `(a₂, b₂) ∘ (a₁, b₁) = (a₂a₁, a₂b₁ + b₂)`로 순서가 있습니다. 이 구현의 `lazy_add`를 이 규칙으로 확장해 보세요.
- 7번은 이 단원에서 가장 어려운 트립 문제입니다. 먼저 6번까지의 구조를 완전히 이해한 뒤 풀이를 읽는 것을 권합니다.
