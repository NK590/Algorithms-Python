"""접미사 자동자(Suffix Automaton, SAM) — 문자열의 모든 부분 문자열을 받아들이는 가장 작은 DFA, 온라인으로 O(n) 에 만들기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 상태 = "끝나는 위치 집합(endpos)이 같은 부분 문자열들의 묶음". 한 상태의 문자열들은 접미사 관계로 이어져 길이가 len[link]+1 .. len 인 연속 구간이다.
  link[v] = 그 묶음에서 가장 짧은 문자열보다 한 글자 더 짧은 (endpos 가 더 큰) 문자열의 상태 → 링크들은 루트(빈 문자열)를 뿌리로 하는 트리(접미사 링크 트리)를 이룬다.
- 글자를 하나씩 붙이는 extend(c): 새 상태 cur 를 만들고, 마지막 상태에서 접미사 링크를 따라 올라가며 c 로 가는 간선이 없는 상태마다 cur 로 가는 간선을 단다.
  이미 c 로 가는 상태 p 를 만나면 q = next[p][c] 를 보고, len[p]+1 == len[q] 면 link[cur] = q, 아니면 q 를 복제(clone)해서 link[cur] = link[q] = clone 으로 분리한다.
  전체 O(n) (분할 상환), 상태 수 ≤ 2n-1 (n ≥ 2), 간선 수 ≤ 3n-4 (n ≥ 3).
- 응용: 서로 다른 부분 문자열의 수(상태마다 len[v] - len[link[v]] 의 합), 부분 문자열 포함 여부와 출현 횟수·위치, 사전순 k 번째 부분 문자열,
  가장 긴 반복 부분 문자열, 두 개 이상의 문자열의 가장 긴 공통 부분 문자열, 가장 짧은 "부분 문자열이 아닌" 문자열.
- 알파벳은 임의의 문자(딕셔너리 간선). 한 객체에서 extend 를 계속 부를 수 있고 계산 결과 캐시는 그때마다 무효화된다.
- 직접 실행하면 Library Checker "Number of Substrings" 형식 — 문자열 하나 — 를 받아 서로 다른 (비어 있지 않은) 부분 문자열의 수를 출력합니다.
"""
import sys
from typing import Iterable, Optional, Sequence


class SuffixAutomaton:
    def __init__(self, text: Iterable[str] = ""):
        self.length = [0]  # len[v]: 상태 v 의 가장 긴 문자열의 길이
        self.link = [-1]
        self.next: list[dict[str, int]] = [{}]
        self.first_end = [-1]  # 상태의 문자열이 처음 나타나는 끝 위치 (복제 상태는 원본의 값을 물려받는다)
        self.is_clone = [False]
        self.last = 0
        self.size = 0  # 지금까지 붙인 글자 수
        self.distinct = 0  # 서로 다른 비어 있지 않은 부분 문자열의 수 (extend 때마다 갱신)
        self._counts: Optional[list[int]] = None  # 출현 횟수 캐시
        self._order: Optional[list[int]] = None  # len 내림차순 상태 순서 캐시
        for ch in text:
            self.extend(ch)

    def _new_state(self, length: int, link: int, transitions: dict[str, int], first_end: int, clone: bool) -> int:
        self.length.append(length)
        self.link.append(link)
        self.next.append(transitions)
        self.first_end.append(first_end)
        self.is_clone.append(clone)
        return len(self.length) - 1

    def extend(self, ch: str) -> None:
        self._counts = self._order = None
        cur = self._new_state(self.length[self.last] + 1, 0, {}, self.size, False)
        p = self.last
        while p != -1 and ch not in self.next[p]:
            self.next[p][ch] = cur
            p = self.link[p]
        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][ch]
            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = self._new_state(self.length[p] + 1, self.link[q], dict(self.next[q]), self.first_end[q], True)
                while p != -1 and self.next[p].get(ch) == q:
                    self.next[p][ch] = clone
                    p = self.link[p]
                self.link[q] = self.link[cur] = clone
        self.last = cur
        self.size += 1
        self.distinct += self.length[cur] - self.length[self.link[cur]]

    @property
    def state_count(self) -> int:
        return len(self.length)

    def transition_count(self) -> int:
        return sum(len(t) for t in self.next)

    def _states_by_length_desc(self) -> list[int]:
        """상태를 len 내림차순으로 (계수 정렬). 링크는 항상 더 짧은 쪽을 가리키므로 자식이 부모보다 먼저 나온다."""
        if self._order is None:
            buckets: list[list[int]] = [[] for _ in range(self.size + 1)]
            for v, length in enumerate(self.length):
                buckets[length].append(v)
            self._order = [v for bucket in reversed(buckets) for v in bucket]
        return self._order

    def _occurrence_counts(self) -> list[int]:
        if self._counts is None:
            counts = [0 if self.is_clone[v] else 1 for v in range(self.state_count)]
            # 루트(상태 0, 빈 문자열) 의 값은 쓰지 않는다: 아래 전파가 루트로는 올리지 않고 count_occurrences("") 는 따로 답한다
            for v in self._states_by_length_desc():
                if self.link[v] > 0:
                    counts[self.link[v]] += counts[v]
            self._counts = counts
        return self._counts

    def _walk(self, pattern: Sequence[str]) -> int:
        """pattern 을 따라간 상태 (부분 문자열이 아니면 -1)."""
        v = 0
        for ch in pattern:
            v = self.next[v].get(ch, -1)
            if v == -1:
                return -1
        return v

    def contains(self, pattern: Sequence[str]) -> bool:
        return self._walk(pattern) != -1

    def count_occurrences(self, pattern: Sequence[str]) -> int:
        """pattern 이 (겹쳐도) 나오는 횟수. 빈 패턴이면 size + 1 (모든 위치)."""
        if len(pattern) == 0:
            return self.size + 1
        v = self._walk(pattern)
        return 0 if v == -1 else self._occurrence_counts()[v]

    def first_occurrence(self, pattern: Sequence[str]) -> int:
        """pattern 이 처음 나오는 시작 위치 (없으면 -1)."""
        v = self._walk(pattern)
        if v == -1:
            return -1
        return self.first_end[v] - len(pattern) + 1

    def occurrence_positions(self, pattern: Sequence[str]) -> list[int]:
        """pattern 이 나오는 모든 시작 위치 (오름차순). 접미사 링크 트리에서 그 상태의 서브트리에 있는, 복제가 아닌 상태들의 끝 위치."""
        if len(pattern) == 0:
            return list(range(self.size + 1))
        v = self._walk(pattern)
        if v == -1:
            return []
        children: list[list[int]] = [[] for _ in range(self.state_count)]
        for u in range(1, self.state_count):
            children[self.link[u]].append(u)
        positions = []
        stack = [v]
        while stack:
            u = stack.pop()
            if not self.is_clone[u]:
                positions.append(self.first_end[u] - len(pattern) + 1)
            stack.extend(children[u])
        return sorted(positions)

    def longest_repeated_substring_length(self) -> int:
        """두 번 이상(겹쳐도) 나오는 가장 긴 부분 문자열의 길이."""
        counts = self._occurrence_counts()
        return max((self.length[v] for v in range(1, self.state_count) if counts[v] >= 2), default=0)

    def kth_distinct_substring(self, k: int) -> str:
        """서로 다른 부분 문자열을 사전순으로 놓았을 때 k 번째 (1 부터)."""
        if not 1 <= k <= self.distinct:
            raise ValueError("k 가 범위를 벗어났습니다")
        paths = [1] * self.state_count  # paths[v] = v 에서 시작하는 서로 다른 경로의 수 (빈 경로 포함)
        for v in self._states_by_length_desc():
            paths[v] = 1 + sum(paths[w] for w in self.next[v].values())
        v, result = 0, []
        while k > 0:
            for ch in sorted(self.next[v]):
                w = self.next[v][ch]
                if k <= paths[w]:
                    result.append(ch)
                    v = w
                    k -= 1  # 지금까지 만든 문자열 자체가 k 번째가 아니었다면 한 칸 소비
                    break
                k -= paths[w]
        return "".join(result)

    def longest_common_substring_with(self, other: Sequence[str]) -> str:
        """이 자동자가 만든 문자열과 other 의 가장 긴 공통 부분 문자열 (같은 길이면 other 에서 먼저 끝나는 것)."""
        v = length = 0
        best_length = best_end = 0
        for i, ch in enumerate(other):
            while v and ch not in self.next[v]:
                v = self.link[v]
                length = self.length[v]
            if ch in self.next[v]:
                v = self.next[v][ch]
                length += 1
            if length > best_length:
                best_length, best_end = length, i + 1
        return "".join(other[best_end - best_length : best_end])

    def shortest_absent_string(self, alphabet: Sequence[str]) -> str:
        """alphabet 위의 문자열 중 부분 문자열이 아닌 것 가운데 가장 짧은 것 (같은 길이면 사전순으로 가장 앞)."""
        letters = sorted(alphabet)
        shortest = [0] * self.state_count
        for v in self._states_by_length_desc():
            shortest[v] = 1 + min((shortest[self.next[v][ch]] if ch in self.next[v] else 0) for ch in letters)
        v, result = 0, []
        while True:
            for ch in letters:
                if ch not in self.next[v]:  # 빠진 글자가 있으면 shortest[v] == 1 이다: 이 글자 하나로 끝
                    return "".join(result) + ch
                if shortest[self.next[v][ch]] == shortest[v] - 1:
                    result.append(ch)
                    v = self.next[v][ch]
                    break


def longest_common_substring_of_many(strings: Sequence[str]) -> str:
    """여러 문자열 모두의 부분 문자열인 가장 긴 문자열 (같은 길이면 첫 문자열에서 먼저 나오는 것)."""
    if not strings:
        return ""
    base = SuffixAutomaton(strings[0])
    bound = list(base.length)  # 각 상태에서 모든 문자열과 동시에 맞출 수 있는 최대 길이 (처음엔 상태의 최장 길이)
    order = base._states_by_length_desc()
    for other in strings[1:]:
        matched = [0] * base.state_count
        v = length = 0
        for ch in other:
            while v and ch not in base.next[v]:
                v = base.link[v]
                length = base.length[v]
            if ch in base.next[v]:
                v = base.next[v][ch]
                length += 1
            matched[v] = max(matched[v], length)
        for u in order:  # 자식에서 맞춘 길이는 부모 상태 전체가 맞춘 것이다 (부모의 문자열은 자식 문자열의 접미사)
            if base.link[u] > 0:
                p = base.link[u]
                matched[p] = base.length[p] if matched[u] > 0 else matched[p]
        bound = [min(b, m) for b, m in zip(bound, matched)]
    best = max(range(base.state_count), key=lambda u: (bound[u], -base.first_end[u]))
    if bound[best] == 0:
        return ""
    end = base.first_end[best] + 1
    return strings[0][end - bound[best] : end]


def count_distinct_substrings(text: str) -> int:
    return SuffixAutomaton(text).distinct


def main() -> None:
    text = sys.stdin.readline().strip()
    print(count_distinct_substrings(text))


if __name__ == "__main__":
    main()
