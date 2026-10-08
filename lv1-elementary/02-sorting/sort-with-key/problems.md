# 연습문제 — 정렬 활용

쉬운 것부터 어려운 순서로 정리했습니다. **문제 지문은 옮기지 않고** 링크와 "배울 점"만 적었습니다. 난이도(solved.ac 티어)는 시간이 지나며 바뀔 수 있어서 표에 적지 않았으니 각 링크에서 확인하세요.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [백준 11650 좌표 정렬하기](https://www.acmicpc.net/problem/11650) | 튜플 정렬 | x 오름차순, 같으면 y 오름차순. `sorted(points)` 한 줄 (`sort_points`) |
| 2 | [백준 1181 단어 정렬](https://www.acmicpc.net/problem/1181) | 여러 기준 + 중복 제거 | 길이순, 같으면 사전순, 중복은 한 번만. [solution.py](solution.py)의 `sort_words`/`main()`이 그대로 풀이다 |
| 3 | [백준 10814 나이순 정렬](https://www.acmicpc.net/problem/10814) | 안정 정렬 | 나이가 같으면 가입한 순서를 유지한다. 나이만 key로 쓰면 안정 정렬이 순서를 지켜 준다 (`sort_by_age`) |
| 4 | [백준 1427 소트인사이드](https://www.acmicpc.net/problem/1427) | 내림차순 | 각 자릿수를 내림차순으로 정렬한다 (`sort_digits_descending`) |
| 5 | [백준 10989 수 정렬하기 3](https://www.acmicpc.net/problem/10989) | 계수 정렬 | 수가 매우 많고 값이 작다. 값별 개수만 세어 출력한다 (`counting_sort`의 아이디어). 메모리에 모든 수를 담지 않는다 |
| 6 | [LeetCode 179 Largest Number](https://leetcode.com/problems/largest-number/) | 비교 함수 | `a+b`와 `b+a`를 비교하는 `cmp_to_key` (`largest_number`) |

## 풀이 메모

- 5번은 메모리 제한이 매우 작아서 입력을 리스트에 모두 담으면 안 됩니다. 입력을 읽는 즉시 개수 배열에 세어야 합니다.
- 3번은 key를 `(나이)`만 주세요. `(나이, 이름)`으로 주면 이름순으로 정렬되어 틀립니다.
