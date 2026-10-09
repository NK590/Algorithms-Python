# 연습문제 — FFT / NTT

아래 순서는 개념의 기본 연산을 익힌 뒤 응용으로 넘어가기 위한 추천 순서입니다. 문제 지문은 원문 링크에서 확인하고, 표의 **배울 점**을 먼저 읽어 어떤 상태와 전이를 사용할지 정리하세요.

[문제 사이트 이용 안내](../../../docs/reference-guide.md)를 참고하세요. `solution.py`는 개념의 참고 구현입니다. 제출 전에는 원문의 입력·출력, 인덱스, 제약 조건에 맞게 호출부를 작성해야 합니다.

| # | 문제 | 유형 | 배울 점 |
|---|---|---|---|
| 1 | [Library Checker — Convolution](https://judge.yosupo.jp/problem/convolution_mod) | 핵심 연습 | 계수 곱의 합을 변환 영역의 점별 곱으로 바꾼다 |
| 2 | [LeetCode 43 Multiply Strings](https://leetcode.com/problems/multiply-strings/) | 문자열 곱셈 | 자릿수 합성곱 + 올림의 기본형. 길이가 작아 이중 반복도 되니 `multiply_decimal_strings`와 비교 |
| 3 | [Library Checker - Convolution (mod 1,000,000,007)](https://judge.yosupo.jp/problem/convolution_mod_1000000007) | 임의 mod 합성곱 | 세 소수 + CRT. 정확한 범위 확인 |
| 4 | [Codeforces 993E Nikita and Order Statistics](https://codeforces.com/problemset/problem/993/E) | `k`개가 `x`보다 작은 부분 배열의 수 | 누적 합 값의 분포를 합성곱 (같은 값 쌍 세기의 변형) |
| 5 | [Codeforces 528D Fuzzy Search](https://codeforces.com/problemset/problem/528/D) | 허용 오차 있는 문자열 매칭 | 문자별 지시 배열의 합성곱 4번. 문자열 → 수열 변환 |

## 연습 순서

1. 기본 연산을 작은 입력에서 손으로 실행하고, 코드의 중간 상태와 비교합니다.
2. 핵심 연습을 풀 때 적용 조건과 시간 복잡도를 먼저 확인합니다. 선행 연습은 해당 도구가 반드시 필요한 문제라는 뜻은 아닙니다.
3. 응용 문제에서는 추가 상태, 자료구조, 전처리가 필요한지 구분하고 작은 입력의 단순한 풀이로 답을 검산합니다.
