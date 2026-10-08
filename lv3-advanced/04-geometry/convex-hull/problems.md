# 연습문제 — 볼록 껍질

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 1708 볼록 껍질](https://www.acmicpc.net/problem/1708) | 기본형 | 껍질의 꼭짓점 수(변 위의 점 제외). [solution.py](solution.py)의 `main()`이 같은 형태 |
| 2 | [LeetCode 587 Erect the Fence](https://leetcode.com/problems/erect-the-fence/) | 변 위의 점 포함 | 울타리 위에 놓이는 모든 나무. `keep_collinear=True`. 모두 일직선인 입력도 있다 |
| 3 | [백준 4181 Convex Hull](https://www.acmicpc.net/problem/4181) | 변 위의 점 + 정해진 순서 | 껍질 위의 모든 점을 특정 시작점과 방향으로 출력. 마지막 변에 일직선 점들이 있을 때 순서가 까다롭다 |
| 4 | [백준 7420 맹독 방벽](https://www.acmicpc.net/problem/7420) | 둘레 | 성곽 둘레와 거리 `L` 이상 떨어진 방벽의 길이 = `둘레 + 2πL`. `hull_perimeter` |
| 5 | [백준 9240 로버트 후드](https://www.acmicpc.net/problem/9240) | 가장 먼 두 점 | 점이 10만 개라 `O(n²)` 불가능. 껍질 + 회전하는 캘리퍼스 (`rotating_calipers_diameter`) |
| 6 | [백준 10254 고속도로](https://www.acmicpc.net/problem/10254) | 가장 먼 두 점 (쌍 출력) | 위와 같은 문제에서 두 점의 좌표를 출력 |
| 7 | [백준 2254 감옥 건설](https://www.acmicpc.net/problem/2254) | 껍질 벗기기 | 껍질을 구하고 그 점들을 지우기를 반복. 지정한 점을 둘러싸는 겹의 수를 센다 |
| 8 | [백준 3878 점 분리](https://www.acmicpc.net/problem/3878) | 분리 가능성 | 두 점 집합의 껍질이 서로 겹치지 않는가: 변의 교차 + 점의 포함 + 퇴화(점·선분) 처리. [선분 교차](../segment-intersection/)와 함께 |

## 풀이 메모

- 1번은 점이 10⁵개입니다. `sys.stdin.buffer.read().split()`로 읽으세요. [테스트](test_solution.py)가 정의("다른 점들의 볼록 결합이 아닌 점")대로 모든 점을 따져 본 결과와 비교합니다.
- 2번, 3번은 `keep_collinear`의 정의입니다. 껍질의 변 위에 있는 점을 포함할 때, 모든 점이 한 직선 위이면 정렬된 모든 점을 그대로 돌려줍니다.
- 5번, 6번의 거리는 제곱으로 비교하고 마지막에만 `sqrt`를 하세요. 6번은 `(거리², p, q)`에서 두 점을 그대로 출력하면 됩니다.
- 7번은 껍질을 벗길 때마다 점이 3개 미만이 되는 퇴화 상황을 확인해야 합니다.
- 4번의 `2πL`은 부동소수점 문제입니다. 출력 형식(정수 반올림)을 확인하세요.
