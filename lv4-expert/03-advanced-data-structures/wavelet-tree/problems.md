# 연습문제 — 웨이블릿 트리

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 7469 K번째 수](https://www.acmicpc.net/problem/7469) | 구간 `k`번째로 작은 수 | 가장 기본형. `kth_smallest`. 퍼시스턴트 세그먼트 트리와 결과 비교 |
| 2 | [Library Checker - Range Kth Smallest](https://judge.yosupo.jp/problem/range_kth_smallest) | 구간 `k`번째 (`n, q ≤ 2·10⁵`, 값이 큼) | [solution.py](solution.py)의 `main()`이 같은 형태. 값 압축은 구조가 알아서 한다 |
| 3 | [백준 13537 수열과 쿼리 1](https://www.acmicpc.net/problem/13537) | 구간에서 `k`보다 큰 수의 개수 | `(길이) − count_at_most`. 질의 값이 배열에 없어도 `bisect`로 순위를 구하면 된다 |
| 4 | [Library Checker - Static Range Frequency](https://judge.yosupo.jp/problem/static_range_frequency) | 구간에서 값 `x`가 나온 횟수 | `count_equal`. 값 하나는 `count_in_range(l, r, x, x)`와 같다 |
| 5 | [백준 14897 서로 다른 수의 개수 2](https://www.acmicpc.net/problem/14897) | 구간에서 서로 다른 수의 개수 | `prev[i]`(이전에 같은 값이 나온 위치)를 배열로 만들고 `prev[i] < l`인 개수 = `count_less(l, r, l)`. 웨이블릿으로 온라인 풀이 (`n = 10⁶`이면 파이썬에서는 오프라인 펜윅 풀이가 더 현실적) |

## 풀이 메모

- 1번과 2번은 같은 문제의 다른 판본입니다. 입력이 클수록 [머지 소트 트리](../merge-sort-tree/)와의 속도 차이가 커집니다 (머지 소트 트리의 `kth_smallest`는 `O(log³ n)`).
- 3번에서 흔한 실수 하나: "`k`보다 큰" 은 `count_at_most`의 여집합입니다. `k`가 배열에 없어도 `bisect_right`가 올바른 한도를 줍니다.
- 직접 해 보기: 가장 작은 `k`개의 합(`sum_smallest`)은 위 문제에 나오지 않는 응용입니다. 임의의 구간과 `k`에 대해 `sorted(a[l:r])[:k]`의 합과 비교하는 테스트를 만들어 보세요 ([test_solution.py](test_solution.py)가 같은 방식으로 검증합니다).
- 5번은 *구간 안에서 처음 나오는 위치* 만 센다는 변환이 핵심입니다. 위치 `i`가 `[l, r)` 안에서 처음 나오는 것 ⟺ `prev[i] < l` (`prev[i]` = 같은 값이 직전에 나온 위치, 없으면 `−1`). 이렇게 만든 `prev` 배열 위에서 `count_less(l, r, l)`가 답입니다.
