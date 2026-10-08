"""solution.py 검증: 순진한 비교와 비교. 모듈러를 일부러 작게 해서 충돌을 많이 만들어도 결과가 정확한지 확인한다"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def search_naive(text, pattern):
    if not pattern:
        return []
    return [i for i in range(len(text) - len(pattern) + 1) if text[i : i + len(pattern)] == pattern]


def random_text(rng, alphabet, max_len):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def test_search_matches_naive():
    rng = random.Random(0)
    for _ in range(1500):
        alphabet = rng.choice(["ab", "abc", "a"])
        text = random_text(rng, alphabet, 30)
        pattern = random_text(rng, alphabet, 6)
        assert solution.rabin_karp(text, pattern) == search_naive(text, pattern), (text, pattern)
    assert solution.rabin_karp("AAAAA", "AA") == [0, 1, 2, 3]
    assert solution.rabin_karp("abc", "") == [] and solution.rabin_karp("ab", "abc") == []


def test_collisions_do_not_cause_false_matches():
    rng = random.Random(1)
    for mod in (2, 3, 7, 11):  # 해시 충돌이 매우 흔하다
        for _ in range(500):
            text = random_text(rng, "abc", 25)
            pattern = random_text(rng, "abc", 5)
            assert solution.rabin_karp(text, pattern, base=5, mod=mod) == search_naive(text, pattern), (text, pattern, mod)


def test_hash_collisions_actually_happen_with_a_small_modulus():
    # 위 테스트가 충돌을 정말로 시험하는지 확인: 'a'(97) 와 'd'(100) 는 mod 3 에서 모두 1 이다
    assert solution.polynomial_hash("a", 5, 3) == solution.polynomial_hash("d", 5, 3) and "a" != "d"


def test_rolling_hash_equals_recomputed_hash():
    rng = random.Random(2)
    for _ in range(100):
        s = random_text(rng, "abcdef", 40)
        m = rng.randint(1, 8)
        if len(s) < m:
            continue
        high = pow(solution.BASE, m - 1, solution.MOD)
        window = solution.polynomial_hash(s[:m])
        for i in range(len(s) - m):
            window = ((window - ord(s[i]) * high) * solution.BASE + ord(s[i + m])) % solution.MOD
            assert window == solution.polynomial_hash(s[i + 1 : i + 1 + m])


def test_prefix_hash_substring_hash_matches_direct_hash():
    rng = random.Random(3)
    for _ in range(100):
        s = random_text(rng, "abc", 30)
        ph = solution.PrefixHash(s)
        for _ in range(30):
            if not s:
                break
            left = rng.randrange(len(s) + 1)
            right = rng.randint(left, len(s))
            assert ph.substring_hash(left, right) == solution.polynomial_hash(s[left:right])
    ph = solution.PrefixHash("abcabc")
    assert ph.substring_hash(0, 3) == ph.substring_hash(3, 6)


def longest_repeated_naive(s):
    for length in range(len(s) - 1, 0, -1):
        seen = set()
        for i in range(len(s) - length + 1):
            sub = s[i : i + length]
            if sub in seen:
                return length
            seen.add(sub)
    return 0


def test_longest_repeated_substring_matches_naive():
    rng = random.Random(4)
    for _ in range(500):
        s = random_text(rng, rng.choice(["ab", "abc"]), 18)
        assert solution.longest_repeated_substring_length(s) == longest_repeated_naive(s), s
    assert solution.longest_repeated_substring_length("banana") == 3  # "ana" (겹쳐도 된다)
    assert solution.longest_repeated_substring_length("abcd") == 0 and solution.longest_repeated_substring_length("") == 0
    assert solution.longest_repeated_substring_length("aaaaa") == 4


def test_small_modulus_still_gives_exact_repeated_substring_length():
    rng = random.Random(5)
    for _ in range(300):
        s = random_text(rng, "abc", 16)
        assert solution.longest_repeated_substring_length(s, base=5, mod=7) == longest_repeated_naive(s), s


def test_has_repeated_substring_rejects_impossible_lengths():
    assert not solution.has_repeated_substring("abcabc", 0) and not solution.has_repeated_substring("abcabc", 7)
    assert solution.has_repeated_substring("abcabc", 3) and not solution.has_repeated_substring("abcabc", 4)


def test_large_input_is_fast():
    text = "ab" * 100_000
    assert len(solution.rabin_karp(text, "abab" * 10)) == 100_000 - 19
    assert solution.longest_repeated_substring_length("xy" * 3000) == 5998


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("ABABABABABABABABABABA\nABABA\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "9"
