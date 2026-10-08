"""solution.py 검증: 패턴마다 본문을 따로 훑는 순진한 방법(겹치는 등장 포함)과 작은 알파벳의 무작위 입력으로 비교"""
import io
import random
from collections import Counter

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def random_string(rng, low, high, alphabet="ab"):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(low, high)))


def naive_occurrences(text, pattern):
    return [i for i in range(len(text) - len(pattern) + 1) if text.startswith(pattern, i)]


def test_find_all_matches_naive_search_for_every_pattern():
    rng = random.Random(0)
    for _ in range(1000):
        alphabet = rng.choice(["a", "ab", "abc"])
        patterns = [random_string(rng, 1, 5, alphabet) for _ in range(rng.randint(1, 6))]  # 중복 패턴, 부분 문자열인 패턴도 나온다
        text = random_string(rng, 0, 25, alphabet)
        automaton = solution.AhoCorasick(patterns)
        expected = sorted((start, index) for index, p in enumerate(patterns) for start in naive_occurrences(text, p))
        assert sorted(automaton.find_all(text)) == expected, (patterns, text)
        assert automaton.count_occurrences(text) == [len(naive_occurrences(text, p)) for p in patterns], (patterns, text)
        assert automaton.contains_any(text) == bool(expected), (patterns, text)


def test_output_links_jump_straight_to_the_nearest_node_that_ends_a_pattern():
    automaton = solution.AhoCorasick(["a", "aaaa"])  # 깊이 2, 3 의 노드는 패턴이 끝나지 않는다
    one, four = automaton.pattern_node
    assert automaton.output_link[four] == one  # 깊이 3 -> 2 -> 1 로 한 칸씩 가지 않고 곧장 "a" 로
    chain = solution.AhoCorasick(["a", "aa", "aaa"])
    ends = chain.pattern_node
    assert chain.output_link[ends[2]] == ends[1] and chain.output_link[ends[1]] == ends[0] and chain.output_link[ends[0]] == 0


def test_find_all_is_ordered_by_end_position_longest_first():
    automaton = solution.AhoCorasick(["a", "ab", "bab", "bc", "bca", "c", "caa"])
    text = "abccab"
    matches = automaton.find_all(text)
    ends = [start + len(automaton.patterns[index]) for start, index in matches]
    assert ends == sorted(ends)
    for (s1, i1), (s2, i2) in zip(matches, matches[1:]):
        if s1 + len(automaton.patterns[i1]) == s2 + len(automaton.patterns[i2]):
            assert len(automaton.patterns[i1]) >= len(automaton.patterns[i2])  # 같은 끝에서는 긴 패턴이 먼저


def test_classic_example_he_she_his_hers():
    automaton = solution.AhoCorasick(["he", "she", "his", "hers"])
    assert sorted(automaton.find_all("ahishers")) == [(1, 2), (3, 1), (4, 0), (4, 3)]
    assert automaton.count_occurrences("ahishers") == [1, 1, 1, 1]
    assert automaton.count_occurrences("shehe") == [2, 1, 0, 0]


def test_failure_links_of_the_classic_automaton():
    automaton = solution.AhoCorasick(["a", "ab", "bab", "bc", "bca", "c", "caa"])
    # 트라이 노드를 문자열로 복원해서 실패 링크가 '가장 긴 진 접미사' 인지 확인한다
    names = {0: ""}
    for node, children in enumerate(automaton.children):
        for ch, child in children.items():
            names[child] = names[node] + ch
    node_names = set(names.values())
    for node, name in names.items():
        if not name:
            continue
        longest = next((name[k:] for k in range(1, len(name) + 1) if name[k:] in node_names), "")
        assert names[automaton.fail[node]] == longest, name


def test_empty_pattern_is_rejected_and_empty_text_is_fine():
    with pytest.raises(ValueError):
        solution.AhoCorasick(["a", ""])
    automaton = solution.AhoCorasick(["ab"])
    assert automaton.find_all("") == [] and automaton.count_occurrences("") == [0] and not automaton.contains_any("")


def test_large_input_matches_substring_counter():
    rng = random.Random(1)
    patterns = [random_string(rng, 6, 10, "abcd") for _ in range(5000)]
    text = random_string(rng, 150_000, 150_000, "abcd")
    automaton = solution.AhoCorasick(patterns)
    counts = automaton.count_occurrences(text)
    lengths = {len(p) for p in patterns}
    substring_counts = Counter(text[i : i + length] for length in lengths for i in range(len(text) - length + 1))
    assert counts == [substring_counts[p] for p in patterns]
    assert len(automaton.find_all(text)) == sum(counts)  # 위치를 모두 나열한 개수와 횟수의 합이 같다
    assert automaton.contains_any(text) and not automaton.contains_any("e" * 1000)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\nabc\nbc\nxyz\n4\nzabcz\nbbb\nxyx\nxyzz\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["YES", "NO", "NO", "YES"]
