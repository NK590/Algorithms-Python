"""웨이블릿 트리(Wavelet Tree) — 구현은 웨이블릿 행렬(Wavelet Matrix): 정적 배열에서 구간의 k 번째 수·x 보다 작은 수의 개수·합을 O(log σ) 에

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 값을 순위(0..m-1, 중복 제거 후 정렬 순서)로 바꾸고 순위를 이진수로 본다. 맨 윗 비트부터 한 층씩, 배열을 "그 비트가 0 인 원소들, 그 다음 1 인 원소들" 로 (순서를 유지하며) 안정적으로 나눈다.
  층마다 "앞에서 i 개 중 0 인 것의 수" zeros[i] 만 저장하면, 구간 [l, r) 이 다음 층에서 어디로 가는지가 zeros 의 차이로 정해진다:
  0 쪽 → [zeros[l], zeros[r]),  1 쪽 → [Z + l - zeros[l], Z + r - zeros[r]]  (Z = 그 층의 0 의 총 수).
- 위에서 아래로 한 번 내려가며 질의에 답한다: k 번째는 "0 쪽 개수 ≥ k 이면 0 쪽, 아니면 k 에서 개수를 빼고 1 쪽", x 보다 작은 수의 개수는 x 의 비트가 1 인 층마다 0 쪽 개수를 더한다.
- 층마다 실제 값의 접두사 합도 저장하면 "구간에서 x 보다 작은 수들의 합", "가장 작은 k 개의 합" 도 같은 방식으로 나온다.
- WaveletMatrix: access, kth_smallest(1 부터), count_less / count_at_most / count_equal / count_in_range, predecessor / successor, sum_less, sum_smallest, median.
  준비 O(n log σ) 시간·메모리, 질의 O(log σ) (σ = 서로 다른 값의 수). 값은 정수. 구간은 모두 반열린 [l, r).
- 직접 실행하면 Library Checker "Range Kth Smallest" 형식 — `N Q`, 수열, 질의 `l r k` (반열린 구간 [l, r), k 는 0 부터) — 를 받아 각 질의의 답을 출력합니다.
"""
import sys
from bisect import bisect_left, bisect_right
from typing import Optional, Sequence


class WaveletMatrix:
    def __init__(self, values: Sequence[int]):
        self.n = len(values)
        self.values = sorted(set(values))  # 순위 -> 값
        rank_of = {v: i for i, v in enumerate(self.values)}
        self.height = max(1, (len(self.values) - 1).bit_length())  # 순위를 나타내는 비트 수
        self.zeros: list[list[int]] = []  # zeros[t][i] = t 번째 층에서 앞의 i 개 중 비트가 0 인 것의 수
        self.zero_total: list[int] = []
        self.prefix_sums: list[list[int]] = []  # prefix_sums[t][i] = t 번째 층(나누기 전) 배열의 앞 i 개 실제 값의 합
        current = [rank_of[v] for v in values]
        for t in range(self.height):
            shift = self.height - 1 - t
            sums = [0]
            for x in current:
                sums.append(sums[-1] + self.values[x])
            self.prefix_sums.append(sums)
            zeros = [0]
            for x in current:
                zeros.append(zeros[-1] + 1 - ((x >> shift) & 1))
            self.zeros.append(zeros)
            self.zero_total.append(zeros[-1])
            current = [x for x in current if not (x >> shift) & 1] + [x for x in current if (x >> shift) & 1]
        sums = [0]
        for x in current:
            sums.append(sums[-1] + self.values[x])
        self.prefix_sums.append(sums)  # 마지막 배열(순위 순으로 안정 정렬된 것)의 접두사 합

    def _check(self, left: int, right: int) -> None:
        if not 0 <= left <= right <= self.n:
            raise IndexError("구간이 범위를 벗어났습니다")

    def access(self, index: int) -> int:
        """a[index]."""
        if not 0 <= index < self.n:
            raise IndexError("index 가 범위를 벗어났습니다")
        rank = 0
        for t in range(self.height):
            zeros = self.zeros[t]
            if zeros[index + 1] - zeros[index]:  # 이 층의 비트가 0
                index = zeros[index]
            else:
                rank |= 1 << (self.height - 1 - t)
                index = self.zero_total[t] + index - zeros[index]
        return self.values[rank]

    def kth_smallest(self, left: int, right: int, k: int) -> int:
        """[left, right) 에서 k 번째(1 부터) 로 작은 값."""
        self._check(left, right)
        if not 1 <= k <= right - left:
            raise ValueError("k 가 범위를 벗어났습니다")
        rank = 0
        for t in range(self.height):
            zeros = self.zeros[t]
            zero_left, zero_right = zeros[left], zeros[right]
            if k <= zero_right - zero_left:
                left, right = zero_left, zero_right
            else:
                k -= zero_right - zero_left
                rank |= 1 << (self.height - 1 - t)
                left, right = self.zero_total[t] + left - zero_left, self.zero_total[t] + right - zero_right
        return self.values[rank]

    def median(self, left: int, right: int) -> int:
        """[left, right) 의 (아래쪽) 중앙값: 정렬했을 때 (길이 + 1) // 2 번째."""
        return self.kth_smallest(left, right, (right - left + 1) // 2)

    def _less_by_rank(self, left: int, right: int, rank_limit: int) -> tuple[int, int]:
        """[left, right) 에서 순위가 rank_limit 보다 작은 원소의 (개수, 값의 합)."""
        self._check(left, right)
        if rank_limit >= 1 << self.height:
            return right - left, self.prefix_sums[0][right] - self.prefix_sums[0][left]
        count = total = 0
        for t in range(self.height):
            zeros = self.zeros[t]
            zero_left, zero_right = zeros[left], zeros[right]
            if (rank_limit >> (self.height - 1 - t)) & 1:  # 한도의 비트가 1: 이 비트가 0 인 원소는 모두 한도보다 작다
                count += zero_right - zero_left
                total += self.prefix_sums[t + 1][zero_right] - self.prefix_sums[t + 1][zero_left]
                left, right = self.zero_total[t] + left - zero_left, self.zero_total[t] + right - zero_right
            else:
                left, right = zero_left, zero_right
        return count, total

    def count_less(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 보다 작은 원소의 수."""
        return self._less_by_rank(left, right, bisect_left(self.values, x))[0]

    def count_at_most(self, left: int, right: int, x: int) -> int:
        return self._less_by_rank(left, right, bisect_right(self.values, x))[0]

    def count_equal(self, left: int, right: int, x: int) -> int:
        return self.count_at_most(left, right, x) - self.count_less(left, right, x)

    def count_in_range(self, left: int, right: int, low: int, high: int) -> int:
        """[left, right) 에서 low ≤ 값 ≤ high 인 원소의 수 (low > high 면 0)."""
        if low > high:
            return 0
        return self.count_at_most(left, right, high) - self.count_less(left, right, low)

    def sum_less(self, left: int, right: int, x: int) -> int:
        """[left, right) 에서 x 보다 작은 원소들의 합."""
        return self._less_by_rank(left, right, bisect_left(self.values, x))[1]

    def predecessor(self, left: int, right: int, x: int) -> Optional[int]:
        """[left, right) 에서 x 보다 작은 값 중 가장 큰 것 (없으면 None)."""
        count = self.count_less(left, right, x)
        return self.kth_smallest(left, right, count) if count else None

    def successor(self, left: int, right: int, x: int) -> Optional[int]:
        """[left, right) 에서 x 보다 큰 값 중 가장 작은 것 (없으면 None)."""
        count = self.count_at_most(left, right, x)
        return self.kth_smallest(left, right, count + 1) if count < right - left else None

    def sum_smallest(self, left: int, right: int, k: int) -> int:
        """[left, right) 에서 가장 작은 k 개의 합 (0 ≤ k ≤ 길이)."""
        self._check(left, right)
        if not 0 <= k <= right - left:
            raise ValueError("k 가 범위를 벗어났습니다")
        if k == 0:
            return 0
        total = rank = 0
        for t in range(self.height):
            zeros = self.zeros[t]
            zero_left, zero_right = zeros[left], zeros[right]
            if k <= zero_right - zero_left:
                left, right = zero_left, zero_right
            else:
                total += self.prefix_sums[t + 1][zero_right] - self.prefix_sums[t + 1][zero_left]
                k -= zero_right - zero_left
                rank |= 1 << (self.height - 1 - t)
                left, right = self.zero_total[t] + left - zero_left, self.zero_total[t] + right - zero_right
        return total + k * self.values[rank]  # 마지막에 남은 k 개는 모두 같은 값


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, q = int(data[0]), int(data[1])
    matrix = WaveletMatrix([int(x) for x in data[2 : 2 + n]])
    out = []
    pos = 2 + n
    for _ in range(q):
        left, right, k = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        out.append(matrix.kth_smallest(left, right, k + 1))
        pos += 3
    print("\n".join(map(str, out)))


if __name__ == "__main__":
    main()
