# 연습문제 — 덱

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10866 덱](https://www.acmicpc.net/problem/10866) | 구현 | push_front/push_back/pop_front/pop_back/size/empty/front/back. [solution.py](solution.py)의 `process_commands`/`main()`이 그대로 풀이다 |
| 2 | [백준 1021 회전하는 큐](https://www.acmicpc.net/problem/1021) | 양방향 회전 | 원소를 앞으로 뽑으려고 왼쪽/오른쪽 중 더 적은 회전을 고른다. 덱의 `rotate`나 양끝 이동 |
| 3 | [백준 5430 AC](https://www.acmicpc.net/problem/5430) | 뒤집기 플래그 | R(뒤집기)을 실제로 하지 않고 방향만 바꾸며, D(앞 지우기)를 덱의 양쪽에서 처리한다 |

## 함께 보면 좋은 문제

- [백준 13549 숨바꼭질 3](https://www.acmicpc.net/problem/13549): 비용이 0 또는 1인 이동. 덱으로 [0-1 BFS](../../../lv2-intermediate/01-shortest-path/zero-one-bfs/)를 하는 첫 문제.

## 풀이 메모

- 3번은 입력 배열이 `[1,2,3]` 같은 문자열이라서 파싱이 까다롭습니다. 대괄호를 벗기고 쉼표로 나누세요.
- 덱은 양끝 접근이 목적이므로 `deque[i]`처럼 가운데를 읽는 풀이는 피하세요.
