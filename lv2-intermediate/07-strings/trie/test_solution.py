"""solution.py 검증: 파이썬 리스트/Counter 로 직접 센 값과 랜덤 비교"""
import io
import itertools
import random
from collections import Counter

from tools.loader import load_solution

solution = load_solution(__file__)


def random_word(rng, alphabet="abc", max_len=5):
    return "".join(rng.choice(alphabet) for _ in range(rng.randint(0, max_len)))


def test_matches_counter_model_with_inserts_and_erases():
    rng = random.Random(0)
    for _ in range(200):
        trie, model = solution.Trie(), Counter()
        for _ in range(rng.randint(0, 40)):
            word = random_word(rng)
            if rng.random() < 0.7:
                trie.insert(word)
                model[word] += 1
            else:
                erased = trie.erase(word)
                assert erased == (model[word] > 0)
                if erased:
                    model[word] -= 1
            assert trie.word_count == sum(model.values())
        for prefix in ["", "a", "b", "ab", "ba", "abc", "cc"]:
            expected = sum(v for w, v in model.items() if w.startswith(prefix))
            assert trie.count_prefix(prefix) == expected, prefix
            assert trie.starts_with(prefix) == (expected > 0)
        for word in ["", "a", "ab", "abc", "bca", "cccc"]:
            assert trie.count(word) == model[word]
            assert (word in trie) == (model[word] > 0)


def test_words_with_prefix_are_sorted_and_distinct():
    rng = random.Random(1)
    for _ in range(200):
        words = [random_word(rng, "abc", 4) for _ in range(rng.randint(0, 15))]
        trie = solution.Trie()
        for w in words:
            trie.insert(w)
        for prefix in ["", "a", "ab", "c"]:
            expected = sorted({w for w in words if w.startswith(prefix)})
            assert trie.words_with_prefix(prefix) == expected, (words, prefix)


def test_readme_example():
    trie = solution.Trie()
    for w in ["app", "apple", "apply", "ape", "bat"]:
        trie.insert(w)
    assert trie.count_prefix("ap") == 4 and trie.count_prefix("app") == 3 and trie.count_prefix("b") == 1
    assert "app" in trie and "ap" not in trie and trie.starts_with("ap")
    assert trie.words_with_prefix("app") == ["app", "apple", "apply"]
    assert trie.erase("apple") and trie.count_prefix("app") == 2 and not trie.erase("apple")


def test_empty_trie_and_empty_word():
    trie = solution.Trie()
    assert trie.count_prefix("") == 0 and "" not in trie and trie.words_with_prefix("") == []
    trie.insert("")
    assert "" in trie and trie.count_prefix("") == 1 and trie.words_with_prefix("") == [""]


def common_prefix_naive(words):
    if not words:
        return ""
    prefix = words[0]
    for w in words[1:]:
        while not w.startswith(prefix):
            prefix = prefix[:-1]
    return prefix


def test_longest_common_prefix():
    rng = random.Random(2)
    for _ in range(500):
        words = [random_word(rng, "ab", 6) for _ in range(rng.randint(0, 6))]
        assert solution.longest_common_prefix(words) == common_prefix_naive(words), words
    assert solution.longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert solution.longest_common_prefix(["dog", "car"]) == "" and solution.longest_common_prefix(["same"]) == "same"


def test_max_xor_pair_matches_pairwise_maximum():
    rng = random.Random(3)
    for _ in range(500):
        numbers = [rng.randint(0, 2**rng.choice([3, 8, 20])) for _ in range(rng.randint(2, 12))]
        expected = max(a ^ b for a, b in itertools.combinations(numbers, 2))
        assert solution.max_xor_pair(numbers) == expected, numbers
    assert solution.max_xor_pair([3, 10, 5, 25, 2, 8]) == 28
    assert solution.max_xor_pair([7, 7]) == 0


def test_max_xor_pair_on_large_input():
    rng = random.Random(4)
    numbers = [rng.randint(0, 2**30) for _ in range(20_000)]
    assert solution.max_xor_pair(numbers) >= max(numbers[0] ^ numbers[1], 0)


def test_many_words_share_a_trie_without_recursion():
    trie = solution.Trie()
    trie.insert("a" * 5000)  # 길이 5000 인 단어도 반복문으로 처리된다
    assert trie.count("a" * 5000) == 1 and trie.count_prefix("a" * 2500) == 1


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3 4\nalgorithmstudy\npython\ntrie\npython\nsample\nalgorithm\ntrie\n"))
    solution.main()
    assert capsys.readouterr().out.strip() == "2"
