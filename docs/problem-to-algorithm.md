# 문제 신호 → 알고리즘 가이드

PS에서 어려운 부분은 구현보다 **"이 문제는 어떤 알고리즘으로 푸는 문제인가"를 알아보는 것**입니다. 문제 조건에 나오는 신호로 후보를 떠올려 보세요. 링크가 없는 항목은 아직 이 저장소에 추가되지 않은 주제입니다.

## 풀기 전에

1. **입력 크기**를 보고 허용되는 복잡도를 가늠합니다. → [복잡도 치트시트](complexity-cheatsheet.md)
2. 작은 예제를 **손으로** 풀어 보고, 그 과정을 일반화할 수 있는지 봅니다.
3. 느리더라도 맞는 풀이(브루트 포스)를 먼저 떠올립니다. 나중에 최적화한 풀이를 검증하는 기준이 됩니다.
4. 경계 조건을 확인합니다. N = 1, 빈 입력, 최댓값, 음수, 중복, 이미 정렬된 입력.

## 신호별 후보

### 탐색 / 완전 탐색

| 문제의 신호 | 후보 |
|---|---|
| N이 작다 (N ≤ 10~20), 모든 경우를 확인해도 된다 | [브루트 포스](../lv0-basics/03-brute-force/brute-force/), [백트래킹](../lv1-elementary/07-algorithm-paradigms/backtracking/), [비트마스크](../lv1-elementary/09-bit-manipulation/bitmask/) |
| 정렬된 데이터에서 값을 찾는다 | [이분 탐색](../lv1-elementary/03-binary-search/binary-search/) |
| "조건을 만족하는 최솟값/최댓값"이고 답을 정하면 가능한지 판정할 수 있다 | 이분 탐색 (매개변수 탐색, 예정) |
| 격자·그래프에서 갈 수 있는지, 영역이 몇 개인지 | [DFS](../lv1-elementary/05-graph-basics/dfs/), [BFS](../lv1-elementary/05-graph-basics/bfs/) |
| 가중치 없는 그래프에서 최소 이동 횟수 | [BFS](../lv1-elementary/05-graph-basics/bfs/) |

### 그래프

| 문제의 신호 | 후보 |
|---|---|
| 최단 거리 / 최소 비용 경로 | [최단 경로 비교표](../lv2-intermediate/01-shortest-path/)에서 가중치 조건으로 선택 |
| 가중치가 0 또는 1 | [0-1 BFS](../lv2-intermediate/01-shortest-path/zero-one-bfs/) |
| 같은 그룹인지 / 그룹 합치기 | [Union-Find](../lv2-intermediate/02-graph-algorithms/union-find/) |
| 작업의 선후 관계, 순서 정하기, 사이클 판정 | [위상 정렬](../lv2-intermediate/02-graph-algorithms/topological-sort/) |
| 모든 정점을 최소 비용으로 연결 | 최소 스패닝 트리 (예정) |

### 구간 / 자료구조

| 문제의 신호 | 후보 |
|---|---|
| 구간 합을 여러 번 묻는다 (값이 바뀌지 않는다) | [누적 합](../lv1-elementary/04-range-techniques/prefix-sum/) |
| 구간 합/최솟값을 묻고 값도 계속 바뀐다 | [세그먼트 트리](../lv3-advanced/01-range-query-structures/segment-tree/) |
| 가장 최근에 넣은 것부터 처리 | [스택](../lv1-elementary/01-data-structures/stack/) |
| 먼저 들어온 것부터 처리 | [큐](../lv1-elementary/01-data-structures/queue/) |
| 양쪽 끝에서 넣고 빼야 한다 | [덱](../lv1-elementary/01-data-structures/deque/) |
| 가장 큰/작은 값을 반복해서 꺼낸다 | [우선순위 큐](../lv1-elementary/01-data-structures/priority-queue/) |
| 존재 여부·개수를 빠르게 확인 | [해시 테이블](../lv1-elementary/01-data-structures/hash-table/) |
| 연속 부분 배열에 조건이 있다 | 투 포인터 / 슬라이딩 윈도우 (예정) |

### 최적화 패러다임

| 문제의 신호 | 후보 |
|---|---|
| 같은 부분 문제가 반복되고, 최댓값/최솟값/경우의 수를 묻는다 | [다이나믹 프로그래밍](../lv1-elementary/07-algorithm-paradigms/dynamic-programming/), [배낭 문제](../lv2-intermediate/04-dynamic-programming/knapsack/) |
| 매 순간 가장 좋아 보이는 선택이 전체 최적이 된다 (증명 필요) | [그리디](../lv1-elementary/07-algorithm-paradigms/greedy/) |
| 문제를 반으로 나눠 같은 문제로 풀 수 있다 | [분할 정복](../lv2-intermediate/05-divide-and-conquer/divide-and-conquer/) |

### 수학 / 문자열

| 문제의 신호 | 후보 |
|---|---|
| 최대공약수, 최소공배수, 서로소 | [유클리드 호제법](../lv1-elementary/06-number-theory/euclidean-algorithm/), [서로소](../lv1-elementary/06-number-theory/relatively-prime/) |
| 소수 판별, 소수 목록, 소인수분해 | [소수 판별](../lv0-basics/02-number-theory/naive-prime-check/), [에라토스테네스의 체](../lv1-elementary/06-number-theory/sieve-of-eratosthenes/), [소인수분해](../lv1-elementary/06-number-theory/prime-factorization/) |
| 큰 수의 나머지, 모듈러 역원 | [페르마의 소정리](../lv2-intermediate/06-number-theory/fermat-little-theorem/), [확장 유클리드](../lv3-advanced/02-number-theory/extended-euclidean-algorithm/) |
| 정수의 이진 표현, XOR | [비트 연산자](../lv1-elementary/09-bit-manipulation/bitwise-operators/) |
| 문자열에서 패턴 찾기 | [KMP](../lv2-intermediate/07-strings/kmp/), [라빈-카프](../lv2-intermediate/07-strings/rabin-karp/) |

## 풀리지 않을 때

- 제한을 다시 읽습니다. 입력 크기가 풀이를 알려 주는 경우가 많습니다.
- 문제를 **그래프 / DP / 정렬 후 탐색** 중 하나로 바꿔서 볼 수 없는지 생각합니다.
- 작은 입력에서 브루트 포스 결과와 내 풀이를 비교하는 **스트레스 테스트**를 만들어 반례를 찾습니다. 이 저장소의 `test_solution.py`가 같은 방식입니다.
