"""정렬 활용 — 내장 정렬에 기준(key)을 주어 여러 조건으로 정렬하기, 그리고 계수 정렬

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 파이썬의 sorted / list.sort 는 안정 정렬(같은 값의 원래 순서 유지)이고, key 함수가 돌려주는 값으로 비교합니다.
- 튜플을 key 로 쓰면 앞 원소부터 차례로 비교하므로 "첫째 기준, 같으면 둘째 기준" 정렬이 됩니다.
- 직접 실행하면 `N` 과 N 개의 단어를 받아, 길이순(같으면 사전순)으로 정렬하고 중복을 없앤 결과를 한 줄씩 출력합니다.
"""
import sys
from functools import cmp_to_key


def sort_words(words: list) -> list:
    """길이가 짧은 순, 같으면 사전순으로 정렬하고 중복은 하나만 남긴다."""
    return sorted(set(words), key=lambda word: (len(word), word))


def sort_points(points: list) -> list:
    """(x, y) 를 x 오름차순, x 가 같으면 y 오름차순으로. 튜플은 앞 원소부터 비교하므로 key 가 필요 없다."""
    return sorted(points)


def sort_by_age(members: list) -> list:
    """(나이, 이름) 목록을 나이순으로. 나이가 같으면 입력 순서(먼저 가입한 사람)를 유지한다. 안정 정렬이라 key 하나로 충분하다."""
    return sorted(members, key=lambda member: member[0])


def sort_digits_descending(n: int) -> int:
    """수의 각 자릿수를 내림차순으로 늘어놓아 만든 수."""
    return int("".join(sorted(str(n), reverse=True)))


def largest_number(numbers: list) -> str:
    """음이 아닌 정수들을 이어 붙여 만들 수 있는 가장 큰 수 (문자열).

    a 를 b 앞에 두는 것이 좋은가는 두 수를 이어 붙인 결과(a+b 와 b+a)를 비교하면 알 수 있다. 이런 규칙은 key 하나로 표현하기 어려워서
    비교 함수를 만들어 cmp_to_key 로 넘긴다.
    """
    def compare(a: str, b: str) -> int:
        if a + b > b + a:
            return -1  # a 가 앞에 오는 것이 더 크다
        if a + b < b + a:
            return 1
        return 0

    result = "".join(sorted(map(str, numbers), key=cmp_to_key(compare)))
    return "0" if result.startswith("0") else result  # [0, 0] 처럼 모두 0 이면 "00" 이 아니라 "0"


def counting_sort(values: list, max_value: int) -> list:
    """0 이상 max_value 이하의 정수를 O(n + max_value) 에 정렬한다. 비교하지 않고 값이 몇 번 나왔는지만 센다."""
    counts = [0] * (max_value + 1)
    for value in values:
        counts[value] += 1
    result = []
    for value, count in enumerate(counts):
        result.extend([value] * count)
    return result


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    print("\n".join(sort_words([input().strip() for _ in range(n)])))


if __name__ == "__main__":
    main()
