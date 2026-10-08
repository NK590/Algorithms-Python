"""solution.py 검증: 문자열 이진 표현·직접 세기·Counter 와 비교"""
import io
import random
from collections import Counter

from tools.loader import load_solution

solution = load_solution(__file__)


def test_readme_example_13_and_10():
    a, b = 13, 10  # 1101, 1010
    assert (a & b, a | b, a ^ b, ~a, a << 1, a >> 1) == (8, 15, 7, -14, 26, 6)
    assert solution.to_binary(13, 8) == "00001101" and solution.to_binary(-14, 8) == "11110010"


def as_string(y):
    """가장 낮은 비트가 0 번째 글자가 되도록 20 비트 문자열로"""
    return format(y, "020b")[::-1]


def test_single_bit_operations_match_string_manipulation():
    rng = random.Random(0)
    for _ in range(500):
        x = rng.randint(0, 2**16)
        i = rng.randint(0, 15)
        bits = as_string(x)
        assert solution.get_bit(x, i) == int(bits[i])
        assert as_string(solution.set_bit(x, i)) == bits[:i] + "1" + bits[i + 1 :]
        assert as_string(solution.clear_bit(x, i)) == bits[:i] + "0" + bits[i + 1 :]
        assert as_string(solution.toggle_bit(x, i)) == bits[:i] + ("0" if bits[i] == "1" else "1") + bits[i + 1 :]


def test_popcount_matches_binary_string_count():
    for x in range(0, 3000):
        assert solution.popcount(x) == bin(x).count("1"), x
    assert solution.popcount(2**100 - 1) == 100 and solution.popcount(0) == 0


def test_is_power_of_two():
    powers = {2**k for k in range(0, 20)}
    for x in range(-5, 5000):
        assert solution.is_power_of_two(x) == (x in powers), x
    assert all(solution.is_power_of_two(p) for p in powers)
    assert not solution.is_power_of_two(2**19 + 1) and not solution.is_power_of_two(-8)


def test_lowest_and_highest_set_bit():
    for x in range(0, 2000):
        low = next((1 << i for i in range(12) if x >> i & 1), 0)
        high = max((1 << i for i in range(12) if x >> i & 1), default=0)
        assert solution.lowest_set_bit(x) == low, x
        assert solution.highest_set_bit(x) == high, x
    assert solution.highest_set_bit(-5) == 0


def test_xor_upto_and_range_match_direct_xor():
    acc = 0
    for n in range(0, 300):
        acc ^= n
        assert solution.xor_upto(n) == acc, n
    assert solution.xor_upto(-1) == 0 and solution.xor_upto(-2) == 0 and solution.xor_upto(-5) == 0  # 빈 범위
    for lo in range(0, 40):
        for hi in range(lo, 40):
            direct = 0
            for v in range(lo, hi + 1):
                direct ^= v
            assert solution.xor_range(lo, hi) == direct, (lo, hi)


def test_single_number_matches_counter():
    rng = random.Random(1)
    for _ in range(300):
        pairs = [rng.randint(0, 50) for _ in range(rng.randint(0, 8))]
        single = rng.randint(100, 200)
        numbers = pairs + pairs + [single]
        rng.shuffle(numbers)
        assert solution.single_number(numbers) == next(v for v, c in Counter(numbers).items() if c == 1)
    assert solution.single_number([4, 1, 2, 1, 2]) == 4


def test_xor_swap():
    for a in range(-5, 20):
        for b in range(-5, 20):
            assert solution.xor_swap(a, b) == (b, a)


def test_count_bits_table_matches_popcount():
    table = solution.count_bits_table(1000)
    assert table == [bin(i).count("1") for i in range(1001)]
    assert solution.count_bits_table(0) == [0]


def test_gray_code_properties():
    for n in range(0, 9):
        codes = solution.gray_code(n)
        assert sorted(codes) == list(range(1 << n))  # 모든 수가 한 번씩
        assert all(bin(a ^ b).count("1") == 1 for a, b in zip(codes, codes[1:]))  # 이웃은 한 비트만 다르다
    assert solution.gray_code(3) == [0, 1, 3, 2, 6, 7, 5, 4]


def test_reverse_bits_matches_string_reverse():
    for width in (1, 4, 8, 16):
        for x in range(0, min(1 << width, 600)):
            assert solution.reverse_bits(x, width) == int(format(x, f"0{width}b")[::-1], 2)
    assert solution.reverse_bits(0b00000110, 8) == 0b01100000


def test_python_negative_numbers_behave_like_twos_complement():
    for x in range(-50, 50):
        assert ~x == -x - 1
        assert solution.to_binary(~x, 16) == format((-x - 1) & 0xFFFF, "016b")
    assert -1 >> 5 == -1 and -8 >> 1 == -4  # 부호가 유지되는 산술 시프트


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("13 10\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["8", "15", "7", "-14", "26", "6"]
