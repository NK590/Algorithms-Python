# 복잡도 치트시트

문제를 읽고 **입력 크기 N부터 보는 습관**을 들이면 풀이 후보가 절반으로 줄어듭니다.

## 1. 입력 크기 → 허용되는 시간 복잡도

시간 제한이 1~2초일 때 C++ 기준으로 단순 연산 약 10^8번 안팎이라는 어림값에서 출발합니다. 상수와 문제에 따라 달라지므로 정확한 기준이 아니라 **후보를 좁히는 용도**입니다.

| N의 크기 | 허용되는 복잡도 | 떠올려 볼 것 |
|---|---|---|
| N ≤ 10 | O(N!) | 순열 완전 탐색, [백트래킹](../lv1-elementary/07-algorithm-paradigms/backtracking/) |
| N ≤ 20 | O(2^N) ~ O(2^N · N) | 부분집합 완전 탐색, [비트마스크](../lv1-elementary/09-bit-manipulation/bitmask/), 비트마스크 DP |
| N ≤ 40 | O(2^(N/2)) | 중간에서 만나기 (meet in the middle) |
| N ≤ 500 | O(N³) | [플로이드-워셜](../lv2-intermediate/01-shortest-path/floyd-warshall/), 3중 반복문 DP |
| N ≤ 5,000 | O(N²) | 2중 반복문 DP, 단순 비교 정렬 |
| N ≤ 10^5 ~ 10^6 | O(N log N) | 정렬, [이분 탐색](../lv1-elementary/03-binary-search/binary-search/), [우선순위 큐](../lv1-elementary/01-data-structures/priority-queue/), [세그먼트 트리](../lv3-advanced/01-range-query-structures/segment-tree/) |
| N ≤ 10^7 | O(N) | [누적 합](../lv1-elementary/04-range-techniques/prefix-sum/), 투 포인터, [에라토스테네스의 체](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/) |
| N ≤ 10^18 | O(log N) | 이분 탐색, 빠른 거듭제곱, [유클리드 호제법](../lv1-elementary/06-number-theory/euclidean-algorithm/) |

그래프 문제는 정점 수 V와 간선 수 E를 함께 봅니다. 예를 들어 V, E가 10^5 정도면 O((V+E) log V)인 [다익스트라](../lv2-intermediate/01-shortest-path/dijkstra/)는 충분하지만, O(V³)인 플로이드-워셜은 불가능합니다.

### 파이썬이라면

CPython은 단순 반복문이 C++보다 수십 배 느립니다. 같은 제한이라면 **위 표에서 N을 한두 단계 낮춰서** 생각하세요. (예: O(N log N)에 N = 10^6이면 CPython으로는 빠듯할 수 있습니다.) PyPy3는 반복문 위주의 코드에서 몇 배 이상 빠른 경우가 많으니 [파이썬으로 PS 하기](python-for-ps.md)를 참고하세요.

## 2. 복잡도별 연산 횟수 감각 (N = 10^6)

| 복잡도 | 대략적인 연산 횟수 |
|---|---|
| O(1) | 1 |
| O(log N) | 20 |
| O(√N) | 1,000 |
| O(N) | 10^6 |
| O(N log N) | 2 × 10^7 |
| O(N²) | 10^12 (불가능) |

## 3. 파이썬 내장 연산의 시간 복잡도

| 연산 | 시간 복잡도 |
|---|---|
| `list[i]`, `list[i] = x`, `len(list)` | O(1) |
| `list.append(x)`, `list.pop()` | O(1) (분할 상환) |
| `list.pop(0)`, `list.insert(0, x)`, 중간 삽입·삭제 | O(n) |
| `x in list`, `list.index(x)`, `list.count(x)` | O(n) |
| `a[i:j]` 슬라이싱 | O(j − i) (복사) |
| `sorted(list)`, `list.sort()` | O(n log n) |
| `min`, `max`, `sum` | O(n) |
| `x in set`, `x in dict`, 삽입·삭제 | 평균 O(1), 최악 O(n) |
| `deque.append`, `appendleft`, `pop`, `popleft` | O(1) |
| `deque[i]` (가운데 접근) | O(n) |
| `heapq.heappush`, `heappop` | O(log n) |
| `heapq.heapify` | O(n) |
| `bisect.bisect_left` 등 | O(log n) (삽입 `insort`는 리스트라 O(n)) |
| 문자열 `s + t` | O(len(s) + len(t)) (매번 새로 복사) |

## 4. 메모리

- 메모리 제한은 보통 128~512MB입니다.
- CPython 리스트는 원소마다 포인터(8바이트)를 가지고, 작은 정수 범위를 벗어나는 정수는 객체(대략 28바이트)로 따로 존재합니다. 그래서 **정수 1천만 개짜리 리스트는 수백 MB**까지 쓸 수 있습니다.
- 크기가 큰 배열이 필요하면 `array` 모듈, `bytearray`, 비트마스크처럼 더 촘촘한 표현을 고려하세요.
