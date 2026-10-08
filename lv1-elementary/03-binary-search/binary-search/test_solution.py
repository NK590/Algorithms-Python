"""solution.py 검증: `in` 연산과 비교 + 탐색 횟수 상한 + 정수 제곱근"""
import io
import math
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def sorted_array(rng):
    return sorted(rng.randint(-10, 10) for _ in range(rng.randint(0, 15)))


def test_readme_example():
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    assert solution.binary_search(arr, 23) == 5
    assert solution.binary_search(arr, 91) == 9
    assert solution.binary_search(arr, 2) == 0
    assert solution.binary_search(arr, 7) == -1


def test_matches_membership_for_every_candidate():
    rng = random.Random(0)
    for _ in range(300):
        arr = sorted_array(rng)
        for target in range(-12, 13):
            for search in (solution.binary_search, solution.binary_search_recursive):
                index = search(arr, target)
                if target in arr:
                    assert index != -1 and arr[index] == target, (arr, target)
                else:
                    assert index == -1, (arr, target)


def test_empty_and_single_element():
    assert solution.binary_search([], 3) == -1
    assert solution.binary_search([3], 3) == 0
    assert solution.binary_search([3], 4) == -1


def test_step_count_is_logarithmic():
    for n in (1, 2, 3, 7, 8, 100, 1000, 100_000):
        arr = list(range(n))
        worst = max(solution.binary_search_steps(arr, t) for t in (-1, 0, n // 2, n - 1, n))
        assert worst <= math.floor(math.log2(n)) + 1, n


def test_integer_sqrt_matches_isqrt():
    for n in range(0, 2000):
        assert solution.integer_sqrt(n) == math.isqrt(n), n
    for n in (10**12, 10**12 + 1, 10**18 - 1, 10**18):
        assert solution.integer_sqrt(n) == math.isqrt(n)


def test_large_array():
    arr = list(range(0, 2_000_000, 2))
    assert solution.binary_search(arr, 1_999_998) == 999_999
    assert solution.binary_search(arr, 1_999_999) == -1


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("5 4\n1 3 5 7 9\n3 4 9 10\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "0", "1", "0"]
