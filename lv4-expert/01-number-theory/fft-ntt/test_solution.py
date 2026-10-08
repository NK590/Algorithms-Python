"""solution.py 검증: 정의대로 계산하는 O(n²) 합성곱·DFT, 파이썬의 큰 정수 곱셈, 완전 탐색과 비교"""
import io
import random
import sys
import time

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)

MOD = solution.MOD


def naive_convolution(a, b):
    if not a or not b:
        return []
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def naive_dft(a, mod, root):
    n = len(a)
    w = pow(root, (mod - 1) // n, mod)
    return [sum(a[j] * pow(w, i * j, mod) for j in range(n)) % mod for i in range(n)]


def test_ntt_matches_the_definition_of_the_discrete_transform():
    rng = random.Random(0)
    for size in (1, 2, 4, 8, 16, 32):
        for mod, root in solution.PRIMES:
            a = [rng.randrange(mod) for _ in range(size)]
            transformed = list(a)
            solution.ntt(transformed, False, mod, root)
            assert transformed == naive_dft(a, mod, root), (size, mod)


def test_inverse_ntt_restores_the_input():
    rng = random.Random(1)
    for size in (1, 2, 8, 64, 1024):
        for mod, root in solution.PRIMES:
            a = [rng.randrange(mod) for _ in range(size)]
            b = list(a)
            solution.ntt(b, False, mod, root)
            solution.ntt(b, True, mod, root)
            assert b == a, (size, mod)


def test_ntt_validates_the_length():
    with pytest.raises(ValueError, match="2 의 거듭제곱"):
        solution.ntt([1, 2, 3])
    with pytest.raises(ValueError, match="지원하지 않습니다"):
        solution.ntt([0] * (2**24), False)  # 998244353 - 1 = 119·2²³ 이라 2²⁴ 길이는 불가능


def test_convolution_mod_matches_the_naive_product():
    rng = random.Random(2)
    for _ in range(120):
        la, lb = rng.randint(1, 40), rng.randint(1, 40)
        a = [rng.randint(-50, MOD + 50) for _ in range(la)]
        b = [rng.randint(0, MOD - 1) for _ in range(lb)]
        expected = [v % MOD for v in naive_convolution(a, b)]
        assert solution.convolution(a, b) == expected, (la, lb)
    assert solution.convolution([], [1, 2]) == [] and solution.convolution([1], []) == []
    assert solution.convolution([3], [4]) == [12]
    assert solution.convolution([1, 1], [1, 1]) == [1, 2, 1]


def test_convolution_uses_the_transform_for_long_inputs_and_agrees_with_the_naive_one():
    rng = random.Random(3)
    for la, lb in [(9, 9), (9, 200), (100, 100), (333, 17), (500, 500)]:
        a = [rng.randrange(MOD) for _ in range(la)]
        b = [rng.randrange(MOD) for _ in range(lb)]
        assert solution.convolution(a, b) == [v % MOD for v in naive_convolution(a, b)], (la, lb)


def test_convolution_with_an_arbitrary_modulus():
    rng = random.Random(4)
    for mod in (2, 7, 1_000_000_007, 10**9 + 9, 10**12 + 39):
        for _ in range(15):
            top = 25 if mod > 10**11 else 60  # 결과 계수의 상한 min(la, lb)·mod² 가 세 소수의 곱의 절반 안에 들어야 한다
            la, lb = rng.randint(1, top), rng.randint(1, top)
            a = [rng.randrange(mod) for _ in range(la)]
            b = [rng.randrange(mod) for _ in range(lb)]
            assert solution.convolution(a, b, mod) == [v % mod for v in naive_convolution(a, b)], (mod, la, lb)
    with pytest.raises(ValueError, match="너무 커서"):
        solution.convolution(list(range(100)), list(range(100)), 10**13)
    # 경계: 길이 9 (NTT 경로) 에서 mod = 10^12 + 39 는 9·10²⁴ 로 한계(≈ 3.9·10²⁵) 안, 길이 50 은 50·10²⁴ = 5·10²⁵ 로 한계 밖
    assert len(solution.convolution([10**12] * 9, [10**12] * 9, 10**12 + 39)) == 17
    with pytest.raises(ValueError, match="너무 커서"):
        solution.convolution([10**12] * 50, [10**12] * 50, 10**12 + 39)


def test_exact_convolution_handles_negative_and_large_coefficients():
    rng = random.Random(5)
    for _ in range(60):
        la, lb = rng.randint(1, 80), rng.randint(1, 80)
        bound = rng.choice([5, 10**4, 10**9])
        a = [rng.randint(-bound, bound) for _ in range(la)]
        b = [rng.randint(-bound, bound) for _ in range(lb)]
        assert solution.convolution_exact(a, b) == naive_convolution(a, b), (la, lb, bound)
    big = [10**11] * 40  # 결과 계수가 40·10²² = 4·10²³ (세 소수의 곱의 절반 안)
    assert solution.convolution_exact(big, big) == naive_convolution(big, big)
    assert solution.convolution_exact([], [5]) == []


def test_fft_convolution_is_exact_for_small_integers():
    rng = random.Random(6)
    for _ in range(80):
        la, lb = rng.randint(1, 60), rng.randint(1, 60)
        a = [rng.randint(-100, 100) for _ in range(la)]
        b = [rng.randint(-100, 100) for _ in range(lb)]
        assert solution.fft_convolution(a, b) == naive_convolution(a, b), (la, lb)
    assert solution.fft_convolution([], [1]) == []
    with pytest.raises(ValueError, match="2 의 거듭제곱"):
        solution.fft([1, 2, 3])


def test_multiply_decimal_strings_matches_python_integers():
    rng = random.Random(7)
    for _ in range(300):
        x = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 60))).lstrip("0") or "0"
        y = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 60))).lstrip("0") or "0"
        assert solution.multiply_decimal_strings(x, y) == str(int(x) * int(y)), (x, y)
    assert solution.multiply_decimal_strings("0", "12345") == "0"
    assert solution.multiply_decimal_strings("99999", "99999") == "9999800001"
    assert solution.multiply_decimal_strings("007", "06") == "42"  # 앞쪽 0 은 무시된다
    with pytest.raises(ValueError, match="숫자로만"):
        solution.multiply_decimal_strings("12a", "3")
    with pytest.raises(ValueError, match="숫자로만"):
        solution.multiply_decimal_strings("-3", "3")


def test_long_decimal_products_are_correct_and_reasonably_fast():
    previous_limit = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)  # 비교용 str(int) 변환의 4300 자리 제한을 푼다
    try:
        _check_long_products()
    finally:
        sys.set_int_max_str_digits(previous_limit)


def _check_long_products():
    rng = random.Random(8)
    x = "".join(rng.choice("0123456789") for _ in range(30000)).lstrip("0")
    y = "".join(rng.choice("0123456789") for _ in range(30000)).lstrip("0")
    started = time.perf_counter()
    assert solution.multiply_decimal_strings(x, y) == str(int(x) * int(y))
    assert time.perf_counter() - started < 15
    nines = "9" * 5000
    assert solution.multiply_decimal_strings(nines, nines) == str(int(nines) ** 2)


def test_max_cyclic_dot_product_matches_trying_every_shift():
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 25)
        a = [rng.randint(-9, 9) for _ in range(n)]
        b = [rng.randint(-9, 9) for _ in range(n)]
        expected = max(sum(a[i] * b[(i + s) % n] for i in range(n)) for s in range(n))
        assert solution.max_cyclic_dot_product(a, b) == expected, (a, b)
    # b = [5, 4, 3, 2, 1] 를 2 칸 밀면 [3, 2, 1, 5, 4]: 3 + 4 + 3 + 20 + 20 = 50 이 최대 (밀기 0..4 의 값: 35, 45, 50, 50, 45)
    assert solution.max_cyclic_dot_product([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]) == 50
    with pytest.raises(ValueError, match="같고"):
        solution.max_cyclic_dot_product([1, 2], [1])
    with pytest.raises(ValueError, match="같고"):
        solution.max_cyclic_dot_product([], [])


def test_count_pair_sums_matches_enumerating_pairs():
    rng = random.Random(10)
    for _ in range(150):
        a = [rng.randint(0, 20) for _ in range(rng.randint(1, 30))]
        b = [rng.randint(0, 20) for _ in range(rng.randint(1, 30))]
        expected = [0] * (max(a) + max(b) + 1)
        for x in a:
            for y in b:
                expected[x + y] += 1
        assert solution.count_pair_sums(a, b) == expected, (a, b)
    assert solution.count_pair_sums([], [1]) == []
    with pytest.raises(ValueError, match="0 이상"):
        solution.count_pair_sums([-1], [1])


def test_ntt_of_a_large_array_is_fast_enough():
    rng = random.Random(11)
    a = [rng.randrange(MOD) for _ in range(2**16)]
    b = list(a)
    started = time.perf_counter()
    solution.ntt(b)
    solution.ntt(b, True)
    assert time.perf_counter() - started < 10
    assert b == a


def test_main_multiplies_two_numbers(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("123456789 987654321\n"))
    solution.main()
    assert capsys.readouterr().out == f"{123456789 * 987654321}\n"
