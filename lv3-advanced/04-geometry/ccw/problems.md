# 연습문제 — CCW와 외적

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11758 CCW](https://www.acmicpc.net/problem/11758) | 기본형 | 세 점의 방향. [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [LeetCode 1232 Check If It Is a Straight Line](https://leetcode.com/problems/check-if-it-is-a-straight-line/) | 일직선 판정 | 첫 두 점과 나머지 점의 `cross`가 모두 0인가 |
| 3 | [LeetCode 812 Largest Triangle Area](https://leetcode.com/problems/largest-triangle-area/) | 삼각형 넓이 | 모든 세 점의 `triangle_area2`의 최댓값. 20개 이하라 완전탐색 |
| 4 | [백준 2166 다각형의 면적](https://www.acmicpc.net/problem/2166) | 신발끈 공식 | `polygon_area2`의 절댓값 / 2. 좌표가 크고 소수점 첫째 자리까지 출력 |
| 5 | [LeetCode 149 Max Points on a Line](https://leetcode.com/problems/max-points-on-a-line/) | 일직선 위의 점 수 | 한 점을 고정하고 다른 점과의 기울기를 기약분수로 센다. 외적으로 직접 판정하는 `O(n³)`과 비교 |
| 6 | [백준 1688 지민이의 테러](https://www.acmicpc.net/problem/1688) | 점이 다각형 안에? | 세 점이 모두 다각형 안(경계 포함)에 있는가. `point_in_polygon`의 경계 처리가 핵심 |
| 7 | [백준 3679 단순 다각형](https://www.acmicpc.net/problem/3679) | 각도순 정렬 | 점들을 한 점 둘레로 각도순 정렬해 단순 다각형을 만든다. 마지막 일직선 구간의 처리가 까다롭다 |

## 풀이 메모

- 1번을 풀 때 `ccw(a, b, c)`의 정의를 종이에 그려 보고, 세 점의 순서를 바꿨을 때 부호가 어떻게 달라지는지 [테스트](test_solution.py)의 `test_cross_properties`와 비교해 보세요.
- 4번은 `area2 = abs(polygon_area2(points))`를 구한 뒤 `area2 // 2`와 `.5` 여부(`area2 % 2`)로 출력하면 부동소수점 오차가 없습니다. 좌표가 `10⁴`를 넘으면 `float`로 곱한 값의 오차가 커져 틀릴 수 있습니다.
- 6번은 경계 위의 점을 "안"으로 볼지가 문제 조건입니다. `point_in_polygon`은 `"inside"`, `"boundary"`, `"outside"`를 구분해 줍니다.
- 7번에서 기준점을 가장 아래(같으면 가장 왼쪽)로 잡고 각도순으로 정렬한 뒤, **마지막 일직선 위의 점들만 거리 역순**으로 뒤집는 처리가 필요합니다. `sort_by_angle`이 각도가 같으면 가까운 점을 먼저 둔다는 점을 이용하세요.
