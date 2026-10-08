# 연습문제 — 대표 그리디 유형

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 틀 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11399 ATM](https://www.acmicpc.net/problem/11399) | ① 정렬 | 짧은 사람부터. 총합은 prefix sum의 합. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 55 Jump Game](https://leetcode.com/problems/jump-game/) | ③ 도달 범위 | `farthest` 하나로 끝난다 (`can_reach_end`) |
| 3 | [백준 1715 카드 정렬하기](https://www.acmicpc.net/problem/1715) | ② 힙 합치기 | 가장 작은 둘을 합치고 다시 넣는다 (`merge_cost`) |
| 4 | [백준 1946 신입 사원](https://www.acmicpc.net/problem/1946) | 정렬 + 최솟값 유지 | 한 점수로 정렬한 뒤, 다른 점수의 최솟값만 추적한다 |
| 5 | [백준 2812 크게 만들기](https://www.acmicpc.net/problem/2812) | ⑤ 스택 | `k`개를 지워 가장 큰 수 (`biggest_after_removing`) |
| 6 | [백준 11000 강의실 배정](https://www.acmicpc.net/problem/11000) | ④ 방 재사용 | 시작 순 정렬 + 끝 시각 최소 힙 (`min_rooms`) |
| 7 | [LeetCode 45 Jump Game II](https://leetcode.com/problems/jump-game-ii/) | ③ 응용 | 최소 점프 수. 현재 점프로 갈 수 있는 끝을 기억하며 BFS 단계처럼 센다 |
| 8 | [백준 2109 순회강연](https://www.acmicpc.net/problem/2109) | 힙 + 마감 | 날짜순으로 보며 강연료를 힙에 쌓고, 넘치면 가장 작은 것을 뺀다 |
| 9 | [백준 1202 보석 도둑](https://www.acmicpc.net/problem/1202) | 정렬 + 힙 | 가방을 작은 순으로, 그 가방에 들어가는 보석 중 가장 비싼 것을 힙에서 꺼낸다 |

## 풀이 메모

- 3번과 8번은 **우선순위 큐**를 쓰는 그리디입니다. `heapq`는 최소 힙이므로 "가장 큰 것"이 필요하면 부호를 바꿔 넣습니다. ([우선순위 큐](../../01-data-structures/priority-queue/))
- 6번과 [활동 선택](../greedy/)을 구별하세요. 6번은 **방의 개수**(시작 순 정렬 + 힙), 활동 선택은 **고를 수 있는 구간의 개수**(끝 순 정렬)입니다.
- 5번은 입력이 크므로 숫자를 정수로 바꾸지 말고 **문자열**로 다루세요.
- 8, 9번은 이 레벨에서 어려운 편입니다. 틀에 익숙해진 뒤 도전하세요.
