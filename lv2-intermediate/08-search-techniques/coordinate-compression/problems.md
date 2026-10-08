# 연습문제 — 좌표 압축

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 18870 좌표 압축](https://www.acmicpc.net/problem/18870) | 기본형 | 각 값을 "자기보다 작은 서로 다른 값의 개수"로. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [LeetCode 1331 Rank Transform of an Array](https://leetcode.com/problems/rank-transform-of-an-array/) | 1부터 시작하는 순위 | `compress` 결과에 1을 더한 값. 같은 값은 같은 순위 |
| 3 | [백준 1015 수열 정렬](https://www.acmicpc.net/problem/1015) | 서수 순위 | 같은 값도 서로 다른 번호, 앞에 나온 것이 앞 (`ordinal_ranks`) |
| 4 | [백준 1517 버블 소트](https://www.acmicpc.net/problem/1517) | 역순쌍 | 버블 정렬의 교환 횟수 = 역순쌍의 개수. 압축 + 펜윅 트리(또는 병합 정렬) |
| 5 | [백준 10090 Counting Inversions](https://www.acmicpc.net/problem/10090) | 역순쌍 | 입력이 1부터 `n`까지의 순열이라 압축이 필요 없다. 펜윅 트리의 기본 연습 |
| 6 | [백준 2517 달리기](https://www.acmicpc.net/problem/2517) | 순위 + 펜윅 트리 | 실력이 같은 선수는 없다. 각 선수의 최선 등수 = 앞 선수 중 자기보다 실력이 좋은 수 + 1 |
| 7 | [LeetCode 315 Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 압축 + 펜윅 트리 | 값을 순위로 바꾸고 뒤에서부터 센다 |
| 8 | [LeetCode 327 Count of Range Sum](https://leetcode.com/problems/count-of-range-sum/) | 접두사 합 압축 | 접두사 합들을 압축하고 `lower ≤ P[j] − P[i] ≤ upper`인 쌍을 센다 |

## 풀이 메모

- 1번은 `ordered = sorted(set(values))` 후 `bisect_left`(또는 딕셔너리)로 풀립니다. 입력이 100만 개이므로 `list.index`는 쓰지 마세요.
- 3번은 2번의 변형입니다. 같은 값 처리가 다르므로 `compress`와 `ordinal_ranks`의 차이를 비교해 보세요.
- 4번~7번은 [펜윅 트리](../../../lv3-advanced/01-range-query-structures/fenwick-tree/)를 배운 뒤에 풀어도 좋습니다. 이 단계에서는 "압축으로 인덱스 범위를 `0..n−1`로 줄인다"까지만 확인하고, 펜윅 트리 대신 병합 정렬로 세는 방법도 가능하다는 것을 알아 두세요(4번).
- 8번은 접두사 합이 음수·큰 수라서 압축이 필수입니다. 접두사 합 `n + 1`개를 압축 대상으로 삼고 구간 `[P[j] − upper, P[j] − lower]`의 양 끝도 함께 이분 탐색할 수 있게 `ordered`를 쓰세요.
- 닫힌 구간의 겹침을 세는 문제는 [solution.py](solution.py)의 `max_overlap_count`처럼 끝에 `r + 1`을 쓰는 것을 잊지 마세요.
