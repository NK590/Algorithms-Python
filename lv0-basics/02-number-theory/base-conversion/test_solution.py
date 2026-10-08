"""solution.py 검증: 파이썬 내장 변환(bin, oct, hex, int(s, base))과 비교 + 음수 진법은 값을 되돌려 확인"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_matches_builtin_bases():
    for n in range(0, 600):
        assert solution.to_base(n, 2) == format(n, "b")
        assert solution.to_base(n, 8) == format(n, "o")
        assert solution.to_base(n, 16) == format(n, "X")
    assert solution.to_base(-10, 2) == "-1010"
    assert solution.to_base(0, 7) == "0"


def test_from_base_matches_int():
    rng = random.Random(0)
    for _ in range(500):
        base = rng.randint(2, 36)
        n = rng.randint(0, 10**6)
        text = solution.to_base(n, base)
        assert solution.from_base(text, base) == n == int(text, base)
        assert solution.from_base(text.lower(), base) == n


def test_roundtrip_including_negatives_and_big_numbers():
    rng = random.Random(1)
    for _ in range(300):
        base = rng.randint(2, 36)
        n = rng.randint(-(10**30), 10**30)
        assert solution.from_base(solution.to_base(n, base), base) == n


def test_known_values():
    assert solution.to_base(255, 16) == "FF"
    assert solution.to_base(35, 36) == "Z"
    assert solution.from_base("ZZZZZ", 36) == 60466175
    assert solution.from_base("-101", 2) == -5


def test_invalid_inputs():
    with pytest.raises(ValueError):
        solution.to_base(5, 1)
    with pytest.raises(ValueError):
        solution.to_base(5, 37)
    with pytest.raises(ValueError):
        solution.from_base("12", 2)  # 2 는 2진법의 숫자가 아니다


def test_negative_base_roundtrip_and_known_values():
    for base in (-2, -3, -10):
        for n in range(-200, 201):
            text = solution.to_negative_base(n, base)
            value = sum(solution.DIGITS.index(ch) * base ** i for i, ch in enumerate(reversed(text)))
            assert value == n, (n, base, text)
            assert text == "0" or text[0] != "0"  # 앞에 불필요한 0 이 없다
    assert solution.to_negative_base(-13, -2) == "110111"
    assert solution.to_negative_base(2, -2) == "110"


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ZZZZZ 36\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "60466175"
