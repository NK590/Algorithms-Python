"""solution.py 검증: 수마다 따로 약수를 구한 값과 비교 + 두 가지 공식 비교"""
import io

from tools.loader import load_solution

solution = load_solution(__file__)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def test_readme_example():
    assert solution.divisor_counts(12)[1:] == [1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6]
    assert solution.divisor_sums(12)[1:] == [1, 3, 4, 7, 6, 12, 8, 15, 13, 18, 12, 28]
    assert solution.divisor_lists(6)[6] == [1, 2, 3, 6]


def test_tables_match_per_number_enumeration():
    n = 400
    counts, sums, lists = solution.divisor_counts(n), solution.divisor_sums(n), solution.divisor_lists(n)
    for k in range(1, n + 1):
        expected = divisors(k)
        assert counts[k] == len(expected) and sums[k] == sum(expected) and lists[k] == expected


def test_sum_of_divisor_sums_matches_two_formulas():
    for n in range(0, 200):
        assert solution.sum_of_divisor_sums(n) == sum(solution.divisor_sums(n)[1:]), n
    assert solution.sum_of_divisor_sums(0) == 0
    assert solution.sum_of_divisor_sums(1) == 1
    assert solution.sum_of_divisor_sums(10) == 87


def test_empty_limit():
    assert solution.divisor_counts(0) == [0]
    assert solution.divisor_lists(0) == [[]]


def test_larger_table():
    sigma = solution.divisor_sums(100_000)
    assert sigma[99_991] == 99_992  # 소수의 약수의 합은 1 + p
    assert sigma[100_000] == 246078


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n1\n2\n10\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["1", "4", "87"]
