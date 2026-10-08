# 연습문제 — 백트래킹

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 15649 N과 M (1)](https://www.acmicpc.net/problem/15649) | 순열 | 중복 없이 M개, `used`로 막는다. `pick_permutations` |
| 2 | [백준 15650 N과 M (2)](https://www.acmicpc.net/problem/15650) | 조합 | 오름차순 수열. 다음 후보를 `start`부터 시작. `pick_combinations` |
| 3 | [백준 15651 N과 M (3)](https://www.acmicpc.net/problem/15651) | 중복 순열 | 같은 수를 여러 번 골라도 된다 → `used`가 필요 없다 |
| 4 | [백준 15652 N과 M (4)](https://www.acmicpc.net/problem/15652) | 중복 조합 | 비내림차순. 다음 후보를 `x`부터(`x + 1`이 아님) 시작 |
| 5 | [LeetCode 78 Subsets](https://leetcode.com/problems/subsets/) | 부분집합 | 각 원소를 넣는다/넣지 않는다. `all_subsets` |
| 6 | [백준 6603 로또](https://www.acmicpc.net/problem/6603) | 조합 | 6개를 고른 조합을 사전 순으로 출력한다 |
| 7 | [백준 1182 부분수열의 합](https://www.acmicpc.net/problem/1182) | 부분집합 | 합이 S인 부분수열의 개수. 공집합 처리에 주의 (S = 0) |
| 8 | [LeetCode 22 Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | 가지치기 | 열린 것 ≥ 닫힌 것이라는 조건으로 가지치기. `generate_parentheses` |
| 9 | [백준 14888 연산자 끼워넣기](https://www.acmicpc.net/problem/14888) | 순열 | 연산자 종류마다 개수를 줄이며 선택, 모든 결과의 최댓값·최솟값 |
| 10 | [백준 14889 스타트와 링크](https://www.acmicpc.net/problem/14889) | 조합 | 팀을 나누는 모든 방법, 팀 능력치의 차이 최소. 대칭을 이용해 절반만 본다 |
| 11 | [백준 1987 알파벳](https://www.acmicpc.net/problem/1987) | 격자 백트래킹 | 지나온 알파벳 집합을 유지하며 DFS. 비트마스크로 줄이기 좋다 |
| 12 | [백준 9663 N-Queen](https://www.acmicpc.net/problem/9663) | 가지치기 | `n_queens_count`. 순수 CPython은 시간이 빠듯하다. 이 폴더의 구현이 어디까지 버티는지 재 보고, 비트마스크 구현이나 PyPy를 고려하자 |
| 13 | [백준 2580 스도쿠](https://www.acmicpc.net/problem/2580) | 가지치기 | 행·열·상자별 사용한 숫자 집합. `solve_sudoku` |
| 14 | [백준 2661 좋은수열](https://www.acmicpc.net/problem/2661) | 일찍 끊기 | 새 숫자를 붙일 때마다 끝부분이 나쁜 수열인지 검사, 사전 순으로 처음 완성된 것이 답 |

## 풀이 메모

- 1~4번은 같은 틀의 네 변형입니다. **순열 vs 조합**, **중복 허용 여부** 두 축만 바꾸면 됩니다. 한 번에 표로 정리해 보세요.
- 7번은 `S = 0`일 때 공집합도 합이 0이라 따로 빼야 합니다.
- 12번은 해답 수가 아니라 **방문 횟수**가 시간을 결정합니다. [README](README.md)의 표(N = 12가 1.1초)를 보고 입력 범위와 비교해 보세요.
- 끝까지 가지 않아도 되는 문제(14번, 스도쿠)는 해를 하나 찾는 즉시 `True`를 반환하게 만드세요.
