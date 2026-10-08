# 연습문제 — 제곱근 분할

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [LeetCode 307 Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 한 점 갱신 + 구간 합 | 블록 합만 갱신하면 되는 가장 단순한 형태. 펜윅 트리와 비교 |
| 2 | [백준 2042 구간 합 구하기](https://www.acmicpc.net/problem/2042) | 한 점 갱신 + 구간 합 | 입력이 크다. 파이썬에서 `√n` 방법과 `O(log n)` 방법의 시간을 비교 |
| 3 | [백준 10999 구간 합 구하기 2](https://www.acmicpc.net/problem/10999) | 구간 더하기 + 구간 합 | `SqrtSum`의 기본형. 값이 `2⁶³`에 가까워 C++에서는 64비트 필요 |
| 4 | [백준 12844 XOR](https://www.acmicpc.net/problem/12844) | 구간 XOR 갱신 + 구간 XOR | `+`가 아니라 XOR이라 블록 `lazy`를 XOR로 합치고, 블록 크기의 홀짝에 따라 `total`이 바뀐다 |
| 5 | [백준 13544 수열과 쿼리 3](https://www.acmicpc.net/problem/13544) | 구간에서 `k`보다 큰 원소 수 (온라인) | 정렬된 복사본 + 이진 탐색. 갱신이 없어 블록 정렬은 한 번 |
| 6 | [백준 17410 수열과 쿼리 1.5](https://www.acmicpc.net/problem/17410) | 한 점 갱신 + `k`보다 큰 원소 수 | [solution.py](solution.py)의 `main()`이 같은 형태(`SqrtCountGreater`) |
| 7 | [Codeforces 13E Holes](https://codeforces.com/problemset/problem/13/E) | 점프 횟수와 마지막 구멍 | 블록마다 "블록을 나갈 때까지의 점프 수와 나가는 위치"를 저장. 갱신은 블록 하나만 다시 계산 |

## 풀이 메모

- 1번과 2번은 [펜윅 트리](../../01-range-query-structures/fenwick-tree/)가 더 알맞은 문제입니다. 제곱근 분할로도 풀어 보고 시간 차이를 확인하세요. 같은 입력이 `O(log n)` 방법은 훨씬 빠릅니다.
- 3번은 [지연 전파 세그먼트 트리](../../01-range-query-structures/lazy-propagation/)로도 풀립니다. 블록에 `lazy`를 두는 이 방법이 코드가 훨씬 짧다는 것을 비교해 보세요.
- 5번은 갱신이 없어서 [머지 소트 트리·웨이블릿 트리](../../../lv4-expert/) 같은 더 강한 도구(Lv4)의 입문 문제이기도 합니다.
- 7번은 "블록 안에서만 일어나는 일은 블록 요약에 담는다"는 제곱근 분할의 일반형을 배우는 문제입니다. 요약이 **합**이 아니라 "함수"인 경우입니다.
