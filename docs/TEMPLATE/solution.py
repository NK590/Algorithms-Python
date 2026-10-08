"""알고리즘 이름 — 핵심 구현

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 알고리즘은 함수로 작성하고, 입력은 인자로 받는다. (test_solution.py 에서 불러다 쓸 수 있도록)
- 표준 입력을 읽는 코드와 예제 실행은 `if __name__ == "__main__":` 아래에만 둔다.
"""
import sys


def solve(values: list[int]) -> int:
    """함수가 무엇을 반환하는지 한 줄로 적는다."""
    # 핵심 로직에는 "무엇을"이 아니라 "왜"를 설명하는 주석을 단다.
    return sum(values)


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    values = list(map(int, input().split()))
    print(solve(values[:n]))


if __name__ == "__main__":
    main()
