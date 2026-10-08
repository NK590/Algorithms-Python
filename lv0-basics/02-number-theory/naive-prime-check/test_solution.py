"""solution.py 검증: 느리지만 확실한 판별(약수의 개수 세기)과의 비교 + 알려진 큰 소수"""
import io

from tools.loader import load_solution

solution = load_solution(__file__)


def divisor_count(n: int) -> int:
    return sum(n % d == 0 for d in range(1, n + 1))


def test_matches_definition_for_small_numbers():
    for n in range(-5, 1500):
        assert solution.is_prime(n) == (n >= 1 and divisor_count(n) == 2), n


def test_edge_cases():
    assert [solution.is_prime(n) for n in (-7, 0, 1, 2, 3, 4)] == [False, False, False, True, True, False]


def test_perfect_squares_of_primes_are_not_prime():
    # √n 까지 검사하는 반복문의 상한이 한 칸 모자라면 p*p 를 소수로 착각한다
    for p in (2, 3, 5, 7, 11, 101, 997):
        assert not solution.is_prime(p * p)
        assert solution.is_prime(p)


def test_large_known_values():
    assert solution.is_prime(1_000_000_007)
    assert solution.is_prime(998_244_353)
    assert not solution.is_prime(1_000_000_007 * 3)
    assert not solution.is_prime(1_000_000_000_000)


def test_slow_version_agrees():
    for n in range(0, 300):
        assert solution.is_prime_slow(n) == solution.is_prime(n)


def test_primes_up_to():
    assert solution.primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert solution.primes_up_to(1) == []
    assert len(solution.primes_up_to(1000)) == 168


def test_main_counts_primes(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("4\n1 3 5 7\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "3"
