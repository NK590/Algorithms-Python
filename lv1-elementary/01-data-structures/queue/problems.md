# 연습문제 — 큐

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 10845 큐](https://www.acmicpc.net/problem/10845) | 구현 | push/pop/size/empty/front/back 명령을 처리한다. `deque`를 쓴다 |
| 2 | [백준 18258 큐 2](https://www.acmicpc.net/problem/18258) | 대량 명령 | 명령이 매우 많다. 리스트의 `pop(0)`을 쓰면 시간 초과가 나고 입력도 빠르게 읽어야 한다 |
| 3 | [백준 2164 카드2](https://www.acmicpc.net/problem/2164) | 큐 시뮬레이션 | [solution.py](solution.py)의 `last_card`/`main()`이 그대로 풀이다. N이 크면 공식 `last_card_formula`로도 풀린다 |
| 4 | [백준 1158 요세푸스 문제](https://www.acmicpc.net/problem/1158) | 원형 제거 | 앞의 K−1명을 뒤로 보내고 K번째를 제거한다. 큐로 그대로 시뮬레이션한다 |

## 풀이 메모

- 2번은 입력이 수십만 줄입니다. [빠른 입출력](../../../lv0-basics/04-io-and-complexity/fast-io/)을 함께 쓰세요.
- 큐를 배웠다면 [BFS](../../05-graph-basics/bfs/)로 이어지는 문제를 풀어 볼 차례입니다.
