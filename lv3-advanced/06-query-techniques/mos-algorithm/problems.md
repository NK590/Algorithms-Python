# 연습문제 — 모스 알고리즘

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [SPOJ DQUERY](https://www.spoj.com/problems/DQUERY/) | 서로 다른 값의 수 | 모스의 기본형. 입력이 1부터이고 양 끝을 포함한다 |
| 2 | [백준 13547 수열과 쿼리 5](https://www.acmicpc.net/problem/13547) | 서로 다른 값의 수 | [solution.py](solution.py)의 `main()`이 같은 형태. `N, M ≤ 10⁵` |
| 3 | [Codeforces 220B Little Elephant and Array](https://codeforces.com/problemset/problem/220/B) | `값 == 등장 횟수`인 값의 수 | 횟수가 바뀔 때마다 조건을 만족하는 값의 수를 같이 갱신한다 |
| 4 | [백준 13548 수열과 쿼리 6](https://www.acmicpc.net/problem/13548) | 최빈값의 빈도 | "횟수의 횟수" 배열을 두어 최댓값을 `O(1)`에 유지한다. `remove`에서 최댓값이 줄어드는 경우 |
| 5 | [Codeforces 617E XOR and Favorite Number](https://codeforces.com/problemset/problem/617/E) | 구간 XOR이 `k`인 부분 구간의 수 | 접두사 XOR을 만들고 쌍의 수를 센다. `add` 때 `count[x ^ k]`를 더한다 |
| 6 | [Codeforces 86D Powerful array](https://codeforces.com/problemset/problem/86/D) | `Σ (등장 횟수)² × 값` | 값이 큰 정수일 때 오버플로가 없는 파이썬의 이점. `add`/`remove`의 증분 계산 |
| 7 | [백준 14897 서로 다른 수와 쿼리 1](https://www.acmicpc.net/problem/14897) | 값이 매우 큰 서로 다른 값의 수 | `N`이 10⁶. 값을 압축해야 하고, 파이썬 모스는 시간이 빠듯하다. 펜윅 트리 오프라인 풀이와 비교 |
| 8 | [백준 13546 수열과 쿼리 4](https://www.acmicpc.net/problem/13546) | 같은 값 사이의 최대 거리 | `remove`가 어렵다. 값마다 위치의 덱을 유지하는 방법과 롤백 모스 |

## 풀이 메모

- 1번과 2번은 같은 문제입니다. 먼저 `len(set(a[l:r]))`로 작은 입력을 풀고, 모스로 같은 답이 나오는지 비교하세요.
- 2번을 파이썬으로 풀면 `n = q = 10⁵`에서 몇 초가 걸립니다([README](README.md#5-복잡도와-입력-크기-가이드)의 측정값). 같은 문제를 [펜윅 트리](../../01-range-query-structures/fenwick-tree/)로 오프라인 풀이(질의를 `r` 순으로 정렬, 각 값의 마지막 등장 위치에만 1)해서 시간을 비교해 보세요.
- 4번은 모스의 상태가 `count[값]` 하나로 부족해서 `count_of_count[횟수]`를 더 유지해야 하는 문제입니다. `add`에서는 최댓값이 늘 수 있고, `remove`에서는 `count_of_count[최댓값]`이 0이 되면 줄어듭니다.
- 5번은 `add(i)` 때 `pairs += count[prefix[i] ^ k]` 같은 식으로 쌍의 수를 갱신합니다. 구간 `[l, r]`의 부분 구간은 접두사 XOR 쌍 `(l−1, r)`로 바뀝니다. 구간의 경계가 한 칸씩 어긋나는 것을 조심하세요.
- 6번과 같은 문제를 일반화한 것이 [README](README.md)의 `equal_pair_counts`입니다. 증분 계산 공식을 직접 유도해 보세요.
