"""solution.py 검증: 1..N 을 하나씩 만들어 보는 순진한 방법, 작은 진법, 닫힌 식과 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def to_base(n, base):
    digits = []
    while n:
        n, r = divmod(n, base)
        digits.append(r)
    return digits[::-1]


def test_digits_of():
    assert solution.digits_of(1) == [1]
    assert solution.digits_of(1234) == [1, 2, 3, 4]
    assert solution.digits_of(10) == [1, 0]
    assert solution.digits_of(10, 2) == [1, 0, 1, 0]
    assert solution.digits_of(255, 16) == [15, 15]


def test_digit_counts_match_writing_out_every_number():
    for n in list(range(0, 300)) + [999, 1000, 1001, 4321, 9999, 10000, 12345]:
        expected = [sum(str(x).count(str(d)) for x in range(1, n + 1)) for d in range(10)]
        assert solution.digit_counts(n) == expected, n
    assert solution.digit_counts(11) == [1, 4, 1, 1, 1, 1, 1, 1, 1, 1]  # BOJ 1019 의 예제
    assert solution.digit_counts(0) == [0] * 10


def test_other_counts_match_brute_force_over_ranges():
    rng = random.Random(0)
    for n in list(range(0, 120)) + [rng.randint(120, 5000) for _ in range(60)]:
        numbers = range(1, n + 1)
        assert solution.digit_sum_total(n) == sum(sum(map(int, str(x))) for x in numbers), n
        banned = rng.randint(0, 9)
        assert solution.count_without_digit(n, banned) == sum(1 for x in numbers if str(banned) not in str(x)), (n, banned)
        target = rng.randint(1, 30)
        assert solution.count_with_digit_sum(n, target) == sum(1 for x in numbers if sum(map(int, str(x))) == target), (n, target)
        k = rng.randint(1, 12)
        assert solution.count_digit_sum_divisible(n, k) == sum(1 for x in numbers if sum(map(int, str(x))) % k == 0), (n, k)
        m = rng.randint(1, 40)
        assert solution.count_multiples(n, m) == n // m, (n, m)
        assert solution.count_no_adjacent_equal(n) == sum(1 for x in numbers if all(a != b for a, b in zip(str(x), str(x)[1:]))), n


def test_other_bases():
    for n in range(0, 200):
        for base in (2, 3, 7):
            expected = sum(to_base(x, base).count(1) for x in range(1, n + 1))
            assert solution.count_digit_occurrences(n, 1, base) == expected, (n, base)
            assert solution.digit_sum_total(n, base) == sum(sum(to_base(x, base)) for x in range(1, n + 1)), (n, base)
            assert solution.count_without_digit(n, 0, base) == sum(1 for x in range(1, n + 1) if 0 not in to_base(x, base)), (n, base)
        expected = sum(1 for x in range(1, n + 1) if "11" not in bin(x))
        assert solution.count_binary_without_adjacent_ones(n) == expected, n
    # 길이 L 의 "1 로 시작하고 11 이 없는" 이진수는 피보나치 F(L) 개(1, 1, 2, 3, 5, …). L = 1..10 의 합은 F(12) - 1 = 143
    assert solution.count_binary_without_adjacent_ones(2**10 - 1) == 143


def test_count_multiples_in_other_bases():
    for n in range(0, 120):
        for base in (2, 3, 7):
            for m in (1, 2, 3, 5, 6):
                assert solution.count_multiples(n, m, base) == n // m, (n, base, m)


def test_huge_n_with_closed_forms():
    for k in range(1, 19):
        n = 10**k - 1
        counts = solution.digit_counts(n)
        assert all(counts[d] == k * 10 ** (k - 1) for d in range(1, 10)), k
        assert sum(counts) == sum(length * 9 * 10 ** (length - 1) for length in range(1, k + 1)), k  # 쓰인 숫자의 총 개수
        assert solution.digit_sum_total(n) == 45 * k * 10 ** (k - 1), k
    n = 10**18
    assert solution.digit_counts(n)[1] == 18 * 10**17 + 1  # 10^18 에서 1 이 하나 더
    assert solution.count_multiples(10**18, 7) == 10**18 // 7
    # 숫자 9 를 쓰지 않는 수: 길이 L 마다 8·9^(L-1) 개 (첫 자리 1..8, 나머지 0..8)
    assert solution.count_without_digit(10**12 - 1, 9) == sum(8 * 9 ** (length - 1) for length in range(1, 13))


def test_count_in_range_and_validation():
    f = lambda n: solution.count_without_digit(n, 4)  # noqa: E731
    assert solution.count_in_range(f, 1, 100) == f(100)
    assert solution.count_in_range(f, 40, 49) == 0
    assert solution.count_in_range(f, 35, 61) == sum(1 for x in range(35, 62) if "4" not in str(x))
    with pytest.raises(ValueError, match="digit"):
        solution.count_digit_occurrences(10, 10)
    with pytest.raises(ValueError, match="진법"):
        solution.digit_dp(10, 0, lambda s, d: (0, 0), base=1)
    with pytest.raises(ValueError, match="k"):
        solution.count_digit_sum_divisible(10, 0)
    with pytest.raises(ValueError, match="m"):
        solution.count_multiples(10, 0)
    assert solution.digit_dp(0, 0, lambda s, d: (0, 0)) == {}
    assert solution.digit_dp(-5, 0, lambda s, d: (0, 0)) == {}


def test_main_prints_ten_counts(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("11\n"))
    solution.main()
    assert capsys.readouterr().out == "1 4 1 1 1 1 1 1 1 1\n"
    monkeypatch.setattr("sys.stdin", io.StringIO("1000000000\n"))
    solution.main()
    zeros = sum(9 * (length - 1) * 10 ** (length - 2) for length in range(2, 10)) + 9  # 1..10^9-1 의 0 과 10^9 의 0 아홉 개
    ones_to_nines = ["900000001"] + ["900000000"] * 8  # 1..10^9-1 에서 각각 9·10^8 번, 1 은 10^9 의 1 이 하나 더
    assert capsys.readouterr().out == " ".join([str(zeros)] + ones_to_nines) + "\n"
    assert zeros == 788888898
