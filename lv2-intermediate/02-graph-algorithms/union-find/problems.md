# 연습문제 — 유니온 파인드

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1717 집합의 표현](https://www.acmicpc.net/problem/1717) | 기본형 | 합치기와 같은 집합 확인. [solution.py](solution.py)의 `main()`이 같은 형태를 처리한다. 재귀 `find`는 깊이 때문에 위험 |
| 2 | [LeetCode 547 Number of Provinces](https://leetcode.com/problems/number-of-provinces/) | 연결 요소 | 인접 행렬의 연결된 쌍을 합치고 남은 집합의 수 (`UnionFind.count`) |
| 3 | [백준 1976 여행 가자](https://www.acmicpc.net/problem/1976) | 연결 확인 | 여행 계획의 모든 도시가 같은 집합인가 |
| 4 | [백준 20040 사이클 게임](https://www.acmicpc.net/problem/20040) | 사이클 탐지 | 처음 사이클이 생기는 순간의 번호 (`first_cycle_edge`) |
| 5 | [LeetCode 684 Redundant Connection](https://leetcode.com/problems/redundant-connection/) | 사이클 간선 | 트리에 간선 하나가 더해진 그래프에서 지울 간선 |
| 6 | [백준 4195 친구 네트워크](https://www.acmicpc.net/problem/4195) | 문자열 + 크기 | 이름을 번호로 바꾸고 합칠 때마다 집합의 크기를 출력. 딕셔너리 |
| 7 | [백준 10775 공항](https://www.acmicpc.net/problem/10775) | 응용 | 비행기를 가능한 가장 큰 번호의 게이트에 배정. 게이트가 차면 그 칸을 왼쪽 칸과 합친다 |
| 8 | [백준 1043 거짓말](https://www.acmicpc.net/problem/1043) | 응용 | 파티마다 참석자를 합치고, 진실을 아는 사람의 집합에 속한 파티는 거짓말할 수 없다 |
| 9 | [LeetCode 721 Accounts Merge](https://leetcode.com/problems/accounts-merge/) | 응용 | 같은 이메일을 가진 계정을 합친다. 이메일 → 번호 매핑 |
| 10 | [백준 2463 비용](https://www.acmicpc.net/problem/2463) | 역순 처리 | 간선을 제거하는 연산을 거꾸로 돌려 합치기로 바꾼다 |

## 풀이 메모

- 1번에서 `find`를 재귀로 쓴 코드가 정점 수가 큰 테스트에서 `RecursionError`로 실패하는 경우가 많습니다. 이 폴더의 반복문 `find`를 쓰세요.
- 4번과 5번은 모두 "간선을 연결한 순간 이미 같은 집합"이 사이클이라는 한 가지 성질을 씁니다.
- 6번처럼 원소가 번호가 아닐 때는 딕셔너리로 이름 → 번호를 만들고, 크기 배열도 함께 관리하세요.
- 10번은 쉽지 않으니 [크루스칼](../kruskal/)과 함께 푸는 것이 좋습니다.
