"""solution.py 검증: 작은 소수에서 모든 점화식을 나열하는 전수 탐색, 무작위 점화식 복원, 행렬 거듭제곱으로 만든 수열과 비교"""
import io
import itertools
import random
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)
P = 998244353


def satisfies(seq, coefficients, mod):
    """정의 그대로: 길이 L 이후의 모든 항이 점화식을 만족."""
    length = len(coefficients)
    for i in range(length, len(seq)):
        total = sum(coefficients[j - 1] * seq[i - j] for j in range(1, length + 1))
        if (seq[i] - total) % mod:
            return False
    return True


def brute_shortest(seq, mod):
    """가장 짧은 길이 L 과, 그 길이에서 가능한 모든 계수의 목록."""
    for length in range(len(seq) + 1):
        found = [list(c) for c in itertools.product(range(mod), repeat=length) if satisfies(seq, c, mod)]
        if found:
            return length, found
    raise AssertionError("unreachable")


def generate(coefficients, initial, count, mod):
    seq = list(initial)
    while len(seq) < count:
        seq.append(sum(coefficients[j] * seq[-1 - j] for j in range(len(coefficients))) % mod)
    return seq


def fibonacci_mod(n, mod):
    def fast(k):
        if k == 0:
            return 0, 1
        a, b = fast(k >> 1)
        c = a * ((2 * b - a) % mod) % mod
        d = (a * a + b * b) % mod
        return (d, (c + d) % mod) if k & 1 else (c, d)

    return fast(n)[0]


def test_matches_exhaustive_search_over_small_fields():
    rng = random.Random(0)
    for mod in (2, 3, 5):
        for _ in range(250 if mod < 5 else 120):
            n = rng.randint(0, 8 if mod < 5 else 6)
            seq = [rng.randrange(mod) for _ in range(n)]
            length, all_valid = brute_shortest(seq, mod)
            result = solution.berlekamp_massey(seq, mod)
            assert len(result) == length, (mod, seq)
            assert result in all_valid, (mod, seq, result)
            if n >= 2 * length:  # 항이 충분하면 점화식은 하나뿐
                assert all_valid == [result]


def test_recovers_random_recurrences_exactly():
    rng = random.Random(1)
    for _ in range(300):
        length = rng.randint(1, 8)
        coefficients = [rng.randrange(P) for _ in range(length)]
        initial = [rng.randrange(P) for _ in range(length)]
        seq = generate(coefficients, initial, 2 * length + rng.randint(0, 5), P)
        result = solution.berlekamp_massey(seq, P)
        assert result == coefficients
        assert satisfies(seq, result, P)


def test_too_few_terms_gives_a_valid_but_different_recurrence():
    lucas_like = generate([1, 1], [1, 3], 12, P)  # 1, 3, 4, 7, 11, 18, ...
    assert solution.berlekamp_massey(lucas_like[:4], P) == [1, 1]
    short = solution.berlekamp_massey(lucas_like[:3], P)  # 2L - 1 = 3 항: 점화식이 유일하지 않다
    assert short == [3, P - 5]  # 3·3 - 5·1 = 4
    assert satisfies(lucas_like[:3], short, P) and not satisfies(lucas_like, short, P)


def test_edge_cases():
    assert solution.berlekamp_massey([], P) == []
    assert solution.berlekamp_massey([0, 0, 0, 0], P) == []
    assert solution.berlekamp_massey([5], P) == [5]
    assert solution.berlekamp_massey([7, 7, 7, 7], P) == [1]
    assert solution.berlekamp_massey([1, 2, 4, 8, 16, 32], P) == [2]
    assert solution.berlekamp_massey([1, 2, 3, 4, 5, 6], P) == [2, P - 1]  # 등차수열: s_i = 2 s_{i-1} - s_{i-2}
    assert len(solution.berlekamp_massey([0, 0, 0, 1], P)) == 4  # 처음 세 항이 0 인 뒤의 1: 길이 4 가 필요
    assert len(solution.berlekamp_massey([0, 0, 1, 2, 4, 8], P)) == 3


def test_values_outside_the_range_are_reduced():
    seq = [1, 2, 4, 8, 16, 32]
    shifted = [x + 3 * P for x in seq]
    negative = [x - 5 * P for x in seq]
    assert solution.berlekamp_massey(shifted, P) == solution.berlekamp_massey(seq, P) == solution.berlekamp_massey(negative, P)


def test_terms_that_are_multiples_of_the_modulus_are_zero():
    fib = generate([1, 1], [0, 1], 10, P)
    shifted = [P] + fib[1:]  # 첫 항이 P (= 0 mod P)
    assert solution.berlekamp_massey(shifted, P) == solution.berlekamp_massey(fib, P) == [1, 1]
    assert solution.berlekamp_massey([P, 2 * P, -3 * P], P) == []


def test_works_for_other_primes():
    rng = random.Random(2)
    for mod in (7, 13, 101, 10**9 + 7):
        for _ in range(60):
            length = rng.randint(1, 5)
            coefficients = [rng.randrange(mod) for _ in range(length)]
            initial = [rng.randrange(mod) for _ in range(length)]
            seq = generate(coefficients, initial, 4 * length + 3, mod)
            result = solution.berlekamp_massey(seq, mod)
            assert len(result) <= length and satisfies(seq, result, mod)
            more = generate(result, seq[: len(result)], 4 * length + 20, mod)
            assert more[: len(seq)] == seq
            assert more == generate(coefficients, initial, 4 * length + 20, mod)


def test_check_recurrence():
    fib = generate([1, 1], [0, 1], 15, P)
    assert solution.check_recurrence(fib, [1, 1], P)
    assert not solution.check_recurrence(fib, [1, 2], P)
    assert solution.check_recurrence([5], [], P) is False
    assert solution.check_recurrence([], [], P) is True
    assert solution.check_recurrence([0, 0, 0], [], P) is True


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) % P for j in range(len(b[0]))] for i in range(len(a))]


def mat_pow(matrix, power):
    size = len(matrix)
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    while power:
        if power & 1:
            result = mat_mul(result, matrix)
        matrix = mat_mul(matrix, matrix)
        power >>= 1
    return result


def random_matrix_sequence(rng, size, count):
    """a_k = u^T M^k v 를 벡터에 행렬을 한 번씩 곱해 만든 수열 (M, u, v 도 함께 돌려준다)."""
    matrix = [[rng.randrange(P) for _ in range(size)] for _ in range(size)]
    u = [rng.randrange(P) for _ in range(size)]
    v = [rng.randrange(P) for _ in range(size)]
    seq, current = [], v
    for _ in range(count):
        seq.append(sum(u[i] * current[i] for i in range(size)) % P)
        current = [sum(matrix[i][j] * current[j] for j in range(size)) % P for i in range(size)]
    return matrix, u, v, seq


def test_matrix_power_sequences_have_recurrence_of_at_most_matrix_size():
    rng = random.Random(3)
    for _ in range(100):
        size = rng.randint(1, 6)
        _, _, _, seq = random_matrix_sequence(rng, size, 60)
        result = solution.berlekamp_massey(seq[: 2 * size], P)
        assert len(result) <= size
        assert satisfies(seq, result, P)  # 앞의 2·size 항에서 찾은 점화식이 60 항 전체에 맞는다


def test_nth_term_after_berlekamp_massey_matches_matrix_power():
    """수열의 앞 2n 항 → 점화식 → 매우 먼 항 = 행렬을 거듭제곱해 직접 구한 u^T M^k v."""
    rng = random.Random(5)
    for _ in range(40):
        size = rng.randint(1, 5)
        matrix, u, v, seq = random_matrix_sequence(rng, size, 2 * size)
        coefficients = solution.berlekamp_massey(seq, P)
        for k in (rng.randrange(10**11, 10**12), 10**18 + rng.randrange(10**6)):
            power = mat_pow(matrix, k)
            direct = sum(u[i] * power[i][j] * v[j] for i in range(size) for j in range(size)) % P
            assert solution.nth_term(coefficients, seq[: len(coefficients)], k, P) == direct


def test_nth_term_matches_direct_generation():
    rng = random.Random(4)
    for _ in range(150):
        length = rng.randint(1, 7)
        coefficients = [rng.randrange(P) for _ in range(length)]
        initial = [rng.randrange(P) for _ in range(length)]
        seq = generate(coefficients, initial, 120, P)
        for k in [0, 1, length - 1, length, length + 1, 37, 119]:
            assert solution.nth_term(coefficients, initial, k, P) == seq[k], (coefficients, k)


def test_nth_term_for_huge_index_matches_fast_doubling_fibonacci():
    for k in [10**9, 10**12, 10**18, 2**61 + 5]:
        for mod in (P, 10**9 + 7):
            assert solution.nth_term([1, 1], [0, 1], k, mod) == fibonacci_mod(k, mod)


def test_nth_term_edge_cases():
    assert solution.nth_term([], [], 5, P) == 0
    assert solution.nth_term([3], [2], 4, P) == 2 * 3**4 % P
    assert solution.nth_term([3], [2], 0, P) == 2


def test_extend_predicts_more_terms():
    squares = [n * n for n in range(8)]
    assert solution.extend(squares, 5, P) == [n * n for n in range(13)]
    fib = generate([1, 1], [0, 1], 6, P)
    assert solution.extend(fib, 10, P) == generate([1, 1], [0, 1], 16, P)
    assert solution.extend([], 3, P) == [0, 0, 0]


def test_random_sequence_has_linear_complexity_about_half_its_length():
    rng = random.Random(6)
    n = 400
    seq = [rng.randrange(P) for _ in range(n)]
    result = solution.berlekamp_massey(seq, P)
    assert len(result) in (n // 2, (n + 1) // 2)
    assert satisfies(seq, result, P)


def test_speed_quadratic_in_length():
    rng = random.Random(7)
    seq = [rng.randrange(P) for _ in range(1500)]
    start = time.perf_counter()
    result = solution.berlekamp_massey(seq, P)
    assert time.perf_counter() - start < 30
    assert satisfies(seq, result, P)


def test_main(monkeypatch, capsys):
    fib = generate([1, 1], [0, 1], 10, P)
    monkeypatch.setattr("sys.stdin", io.StringIO(f"10\n{' '.join(map(str, fib))}\n"))
    solution.main()
    assert capsys.readouterr().out.split("\n")[:2] == ["2", "1 1"]
