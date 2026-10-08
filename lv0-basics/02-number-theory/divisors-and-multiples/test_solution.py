"""solution.py 검증: O(n) 방식과의 비교 + 제곱수·소수 같은 경계"""
import io

from tools.loader import load_solution

solution = load_solution(__file__)


def test_divisors_match_slow_version():
    for n in range(1, 2000):
        assert solution.divisors(n) == solution.divisors_slow(n), n


def test_perfect_squares_do_not_duplicate_the_root():
    assert solution.divisors(36) == [1, 2, 3, 4, 6, 9, 12, 18, 36]
    assert solution.divisors(1) == [1]
    assert solution.divisors(49) == [1, 7, 49]


def test_primes_have_two_divisors():
    assert solution.divisors(97) == [1, 97]


def test_large_input_uses_square_root_loop():
    assert solution.divisors(10**12)[-1] == 10**12
    assert len(solution.divisors(10**12)) == 169  # (2^12)(5^12) → (12+1)(12+1)


def test_multiples():
    assert solution.multiples(3, 20) == [3, 6, 9, 12, 15, 18]
    assert solution.multiples(5, 4) == []


def test_perfect_numbers():
    assert [n for n in range(1, 10000) if solution.is_perfect_number(n)] == [6, 28, 496, 8128]


def test_kth_divisor():
    assert solution.kth_divisor(6, 3) == 3
    assert solution.kth_divisor(6, 5) == 0
    assert solution.kth_divisor(1, 1) == 1


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("6 3\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
