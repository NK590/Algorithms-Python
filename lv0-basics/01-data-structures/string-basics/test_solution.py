"""solution.py 검증: 파이썬 내장 기능과의 랜덤 비교"""
import io
import random
import string
from collections import Counter

from tools.loader import load_solution

solution = load_solution(__file__)


def random_text(rng, alphabet="abAB c", max_len=10):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def test_is_palindrome_matches_slicing():
    rng = random.Random(0)
    for _ in range(500):
        s = random_text(rng, "ab", 8)
        assert solution.is_palindrome(s) == (s == s[::-1]), s
    assert solution.is_palindrome("") and solution.is_palindrome("a") and solution.is_palindrome("level")
    assert not solution.is_palindrome("ab")


def test_char_counts_matches_counter_and_keeps_first_seen_order():
    rng = random.Random(1)
    for _ in range(300):
        s = random_text(rng)
        assert solution.char_counts(s) == dict(Counter(s))
        assert list(solution.char_counts(s)) == list(dict.fromkeys(s))


def test_reverse_words():
    assert solution.reverse_words("I love you") == "you love I"
    assert solution.reverse_words("  a   b  ") == "b a"
    assert solution.reverse_words("") == ""


def test_caesar_shift_examples_and_roundtrip():
    assert solution.caesar_shift("abc xyz", 3) == "def abc"
    assert solution.caesar_shift("Hello, World!", 13) == "Uryyb, Jbeyq!"
    rng = random.Random(2)
    for _ in range(300):
        s = random_text(rng, string.ascii_letters + " ,.")
        k = rng.randint(-30, 30)
        assert solution.caesar_shift(solution.caesar_shift(s, k), -k) == s
        assert solution.caesar_shift(s, 26) == s


def test_is_anagram():
    assert solution.is_anagram("listen", "silent")
    assert not solution.is_anagram("aab", "abb")
    rng = random.Random(3)
    for _ in range(300):
        a, b = random_text(rng, "abc", 6), random_text(rng, "abc", 6)
        assert solution.is_anagram(a, b) == (sorted(a) == sorted(b))


def test_main_prints_1_for_palindrome(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("level\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "1"
    monkeypatch.setattr("sys.stdin", io.StringIO("level up\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "0"
