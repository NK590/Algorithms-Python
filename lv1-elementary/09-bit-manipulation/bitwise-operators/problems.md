# 연습문제 — 비트 연산자

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [CSES — Bit Strings](https://cses.fi/problemset/task/1617) | 핵심 연습 | 비트 하나의 두 선택을 경우의 수와 연결한다 |
| 2 | [CSES — Gray Code](https://cses.fi/problemset/task/2205) | 핵심 연습 | XOR로 그레이 코드를 구성한다 |
| 3 | [LeetCode 191 Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits/) | popcount | `x & (x−1)` 반복 (`popcount`) |
| 4 | [LeetCode 231 Power of Two](https://leetcode.com/problems/power-of-two/) | 판별 | `x > 0 and x & (x−1) == 0` (`is_power_of_two`) |
| 5 | [LeetCode 136 Single Number](https://leetcode.com/problems/single-number/) | XOR | 모두 XOR하면 한 번만 나온 수가 남는다 (`single_number`) |
| 6 | [LeetCode 338 Counting Bits](https://leetcode.com/problems/counting-bits/) | DP | `bits[i] = bits[i >> 1] + (i & 1)` (`count_bits_table`) |
| 7 | [LeetCode 461 Hamming Distance](https://leetcode.com/problems/hamming-distance/) | XOR + popcount | 다른 비트의 수 = `popcount(a ^ b)` |
| 8 | [LeetCode 268 Missing Number](https://leetcode.com/problems/missing-number/) | XOR | 0..n과 배열을 모두 XOR하면 빠진 수만 남는다 |
| 9 | [LeetCode 190 Reverse Bits](https://leetcode.com/problems/reverse-bits/) | 비트 뒤집기 | 폭을 고정해 한 비트씩 옮긴다 (`reverse_bits`) |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
