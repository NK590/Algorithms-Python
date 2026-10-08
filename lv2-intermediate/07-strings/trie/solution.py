"""트라이(Trie, 접두사 트리) — 문자열을 글자 하나씩 간선으로 하는 트리에 저장해 접두사 질의를 O(길이) 에 처리하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 루트에서 글자를 따라 내려가면 접두사가 되고, "여기서 끝나는 단어가 있다"는 표시(is_end)로 단어를 구분합니다.
- 노드마다 이 노드를 지나는 단어의 수(passing)를 저장하면 "이 접두사로 시작하는 단어가 몇 개인가"를 O(접두사 길이) 에 답할 수 있습니다.
- 숫자를 이진수로 보고 글자를 비트로 삼으면 "XOR 이 최대인 두 수" 같은 문제도 트라이로 풉니다.
- 직접 실행하면 `N M`, N 개의 문자열(집합 S), M 개의 문자열을 받아 M 개 중 S 에 포함된 문자열의 수를 출력합니다.
"""
import sys


class Trie:
    def __init__(self):
        # 노드는 [자식 딕셔너리, 단어가 여기서 끝나는 횟수, 이 노드를 지나는 단어 수] 로 표현한다
        self.children: list[dict[str, int]] = [{}]
        self.end_count: list[int] = [0]
        self.passing: list[int] = [0]
        self.word_count = 0

    def _new_node(self) -> int:
        self.children.append({})
        self.end_count.append(0)
        self.passing.append(0)
        return len(self.children) - 1

    def insert(self, word: str) -> None:
        """단어를 넣는다. 같은 단어를 여러 번 넣으면 횟수가 센다."""
        node = 0
        self.passing[0] += 1
        for ch in word:
            nxt = self.children[node].get(ch)
            if nxt is None:
                nxt = self._new_node()
                self.children[node][ch] = nxt
            node = nxt
            self.passing[node] += 1
        self.end_count[node] += 1
        self.word_count += 1

    def _walk(self, text: str) -> int:
        """text 를 따라 내려간 노드 번호. 중간에 막히면 -1."""
        node = 0
        for ch in text:
            node = self.children[node].get(ch, -1)
            if node == -1:
                return -1
        return node

    def count(self, word: str) -> int:
        """정확히 이 단어가 몇 번 들어 있는가."""
        node = self._walk(word)
        return 0 if node == -1 else self.end_count[node]

    def __contains__(self, word: str) -> bool:
        return self.count(word) > 0

    def count_prefix(self, prefix: str) -> int:
        """이 접두사로 시작하는 단어(중복 포함)의 수."""
        node = self._walk(prefix)
        return 0 if node == -1 else self.passing[node]

    def starts_with(self, prefix: str) -> bool:
        return self.count_prefix(prefix) > 0

    def erase(self, word: str) -> bool:
        """단어 하나를 지운다(중복이면 한 번만). 없으면 False. 지나온 노드의 passing 을 줄이므로 count_prefix 가 계속 맞다."""
        if word not in self:
            return False
        node = 0
        self.passing[0] -= 1
        for ch in word:
            node = self.children[node][ch]
            self.passing[node] -= 1
        self.end_count[node] -= 1
        self.word_count -= 1
        return True

    def words_with_prefix(self, prefix: str) -> list[str]:
        """prefix 로 시작하는 서로 다른 단어를 사전순으로. 접두사 노드에서 DFS(자식을 글자 순으로)한다."""
        start = self._walk(prefix)
        if start == -1:
            return []
        result = []
        stack = [(start, prefix)]
        while stack:
            node, text = stack.pop()
            if self.end_count[node] > 0:
                result.append(text)
            for ch in sorted(self.children[node], reverse=True):  # 스택이라 거꾸로 넣어야 사전순으로 나온다
                stack.append((self.children[node][ch], text + ch))
        return result


def longest_common_prefix(words: list[str]) -> str:
    """모든 단어의 공통 접두사. 트라이에 넣고, 자식이 하나뿐이고 단어가 끝나지 않는 동안 내려간다."""
    if not words:
        return ""
    trie = Trie()
    for w in words:
        trie.insert(w)
    prefix = []
    node = 0
    while len(trie.children[node]) == 1 and trie.end_count[node] == 0:
        (ch, node), = trie.children[node].items()
        prefix.append(ch)
    return "".join(prefix)


def max_xor_pair(numbers: list[int], bits: int = 31) -> int:
    """두 수의 XOR 의 최댓값 (수가 둘 이상). 수를 이진수 문자열(높은 비트부터)로 보고 트라이에 넣은 뒤,
    각 수마다 '반대 비트' 쪽 자식을 우선해 내려가면 그 수와 XOR 이 최대인 짝을 찾는다."""
    children: list[list[int]] = [[-1, -1]]

    def insert(x):
        node = 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            if children[node][bit] == -1:
                children.append([-1, -1])
                children[node][bit] = len(children) - 1
            node = children[node][bit]

    for x in numbers:
        insert(x)
    best = 0
    for x in numbers:
        node, value = 0, 0
        for b in range(bits - 1, -1, -1):
            bit = x >> b & 1
            want = 1 - bit  # 반대 비트로 가면 XOR 의 이 자리가 1 이 된다
            if children[node][want] != -1:
                value |= 1 << b
                node = children[node][want]
            else:
                node = children[node][bit]
        best = max(best, value)
    return best


def main() -> None:
    input = sys.stdin.readline
    n, m = map(int, input().split())
    trie = Trie()
    for _ in range(n):
        trie.insert(input().strip())
    print(sum(1 for _ in range(m) if input().strip() in trie))


if __name__ == "__main__":
    main()
