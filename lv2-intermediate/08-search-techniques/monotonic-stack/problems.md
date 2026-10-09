# 연습문제 — 모노톤 스택

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Nearest Smaller Values](https://cses.fi/problemset/task/1645) | 핵심 연습 | 이전의 더 작은 원소를 스택에서 찾는다 |
| 2 | [CSES — Increasing Array Queries](https://cses.fi/problemset/task/2416) | 심화·응용 | 심화로 정렬된 후보 경계와 구간 비용을 연결한다 |
| 3 | [LeetCode 739 Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | 위치 차이 | 오큰수의 거리. `days_until_warmer` |
| 4 | [LeetCode 503 Next Greater Element II](https://leetcode.com/problems/next-greater-element-ii/) | 원형 배열 | 수열을 두 번 훑는다 (인덱스 `i % n`) |
| 5 | [LeetCode 42 Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | 빗물 | 스택으로 층별 계산 (`trapped_rain_water`), 양쪽 최댓값 배열이나 투 포인터로도 풀린다 |
| 6 | [LeetCode 402 Remove K Digits](https://leetcode.com/problems/remove-k-digits/) | 그리디 + 스택 | 앞 자리가 크면 pop하는 오름차순 스택, 남은 `k`는 끝에서 제거 |
| 7 | [LeetCode 907 Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums/) | 기여도 계산 | 각 원소가 최솟값인 구간의 왼쪽·오른쪽 한계를 스택으로 구해 `값 × 왼쪽 개수 × 오른쪽 개수`. 중복 값은 한쪽만 `≤` |
| 8 | [LeetCode 85 Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | 히스토그램으로 환원 | 행마다 위로 연속한 1의 개수를 막대 높이로 하는 히스토그램 문제 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
