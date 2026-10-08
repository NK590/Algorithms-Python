"""solution.py 검증: 내장 메서드와의 랜덤 비교 + 왕복 변환"""
import io
import os
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_run_length_examples():
    assert solution.run_length_encode("aaabcc") == "a3b1c2"
    assert solution.run_length_encode("") == ""
    assert solution.run_length_encode("z") == "z1"
    assert solution.run_length_decode("a3b1c2") == "aaabcc"
    assert solution.run_length_decode("x12") == "x" * 12


def test_run_length_roundtrip():
    rng = random.Random(0)
    for _ in range(500):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 30)))
        assert solution.run_length_decode(solution.run_length_encode(s)) == s


def test_longest_common_prefix():
    assert solution.longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert solution.longest_common_prefix(["dog", "racecar"]) == ""
    assert solution.longest_common_prefix(["same"]) == "same"
    assert solution.longest_common_prefix([]) == ""
    rng = random.Random(1)
    for _ in range(300):
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 5))) for _ in range(rng.randint(1, 4))]
        assert solution.longest_common_prefix(words) == os.path.commonprefix(words)


def test_count_words_matches_split():
    rng = random.Random(2)
    for _ in range(500):
        s = "".join(rng.choice("ab  ") for _ in range(rng.randint(0, 15)))
        assert solution.count_words(s) == len(s.split()), repr(s)


def test_split_by_matches_str_split():
    rng = random.Random(3)
    for _ in range(500):
        s = "".join(rng.choice("ab,;") for _ in range(rng.randint(0, 12)))
        for sep in (",", ";,", "a"):
            assert solution.split_by(s, sep) == s.split(sep), (s, sep)


@pytest.mark.parametrize("text, expected", [
    ("ljes=njak", 6), ("ddz=z=", 3), ("nljj", 3), ("c=c=", 2), ("dz=ak", 3), ("", 0), ("abc", 3),
])
def test_count_croatian(text, expected):
    assert solution.count_croatian(text) == expected


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ljes=njak\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "6"
