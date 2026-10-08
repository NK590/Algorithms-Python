# 연습문제 — 위상 정렬

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 2252 줄 세우기](https://www.acmicpc.net/problem/2252) | 기본형 | 키 비교 관계를 모두 지키는 줄. 정답이 여러 개(검사기). [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다 |
| 2 | [LeetCode 207 Course Schedule](https://leetcode.com/problems/course-schedule/) | 사이클 판별 | 모든 과목을 들을 수 있는가 = 사이클이 없는가 (`has_cycle`) |
| 3 | [LeetCode 210 Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | 순서 구하기 | 수강 순서 하나 출력, 불가능하면 빈 배열 |
| 4 | [백준 1766 문제집](https://www.acmicpc.net/problem/1766) | 사전순 최소 | 쉬운 문제(작은 번호)를 먼저. 최소 힙. `smallest_topological_order` |
| 5 | [백준 2623 음악프로그램](https://www.acmicpc.net/problem/2623) | 순서 구하기 + 사이클 | 여러 목록의 순서를 하나의 그래프로 합치고 불가능하면 0 |
| 6 | [백준 2056 작업](https://www.acmicpc.net/problem/2056) | DAG DP | 선행 작업이 끝나야 시작할 때 모든 작업이 끝나는 최소 시간. `earliest_finish_times` |
| 7 | [백준 1005 ACM Craft](https://www.acmicpc.net/problem/1005) | DAG DP | 특정 건물을 짓는 최소 시간 (테스트 케이스 여러 개) |
| 8 | [백준 1516 게임 개발](https://www.acmicpc.net/problem/1516) | DAG DP | 건물마다 완성까지 걸리는 시간 |
| 9 | [백준 3665 최종 순위](https://www.acmicpc.net/problem/3665) | 응용 | 작년 순위에서 몇 쌍만 뒤바뀐 올해 순위를 구하거나 판별 불가/데이터 오류를 구분 |
| 10 | [백준 1948 임계경로](https://www.acmicpc.net/problem/1948) | 임계 경로 | 가장 오래 걸리는 경로의 시간과 그 경로 위의 간선 수. 역방향 그래프가 필요 |

## 풀이 메모

- 1번은 출력이 여러 개일 수 있으므로 자신의 출력과 예시 출력을 단순 비교하지 마세요. 모든 간선이 지켜졌는지 직접 확인하면 됩니다. 이 폴더의 [테스트](test_solution.py)도 같은 방법입니다.
- 6~8번은 모두 `finish[v] = 자기 시간 + max(선행 finish)` 한 줄이 핵심입니다.
- 5번과 9번은 "같은 순서가 두 개"일 수 있어 문제 조건(데이터 오류, 불가능)을 꼼꼼히 읽어야 합니다.
- 10번은 최장 경로를 구한 뒤, 간선을 뒤집은 그래프에서 도착점으로부터 거슬러 올라가며 최장 경로 위의 간선만 셉니다.
