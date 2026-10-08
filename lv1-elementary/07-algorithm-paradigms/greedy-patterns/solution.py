"""대표 그리디 유형 — 정렬 / 힙 / 스택으로 "지금 최선"을 빠르게 고르는 다섯 가지 틀

README.md 의 설명과 짝을 이루는 참고 구현입니다.
1. 정렬해서 순서를 정하기       : min_total_wait    (ATM)
2. 가장 작은 둘을 합치기(힙)     : merge_cost        (카드 정렬하기)
3. 가장 멀리 갈 수 있는 곳 갱신   : can_reach_end     (점프)
4. 끝난 방을 재사용하기(힙)      : min_rooms         (강의실 배정)
5. 앞의 작은 숫자를 지우기(스택)  : biggest_after_removing (크게 만들기)
- 직접 실행하면 `N` 과 N 개의 처리 시간을 받아 모든 사람의 대기 시간 합의 최솟값을 출력합니다.
"""
import heapq
import sys


def min_total_wait(times: list) -> int:
    """한 줄로 서서 한 명씩 처리받을 때, 모든 사람이 끝나는 시각의 합의 최솟값.

    처리 시간이 짧은 사람을 앞에 세운다. i 번째 사람의 시간은 뒤의 (n - i) 명에게 모두 더해지기 때문이다."""
    total = elapsed = 0
    for t in sorted(times):
        elapsed += t
        total += elapsed
    return total


def merge_cost(sizes: list) -> int:
    """묶음들을 둘씩 합쳐 하나로 만들 때 (합치는 비용 = 두 크기의 합) 총 비용의 최솟값.

    항상 가장 작은 두 묶음을 합친다. 먼저 합친 묶음은 여러 번 비용에 더해지므로 작은 것을 먼저 합쳐야 한다."""
    heap = list(sizes)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        merged = heapq.heappop(heap) + heapq.heappop(heap)
        total += merged
        heapq.heappush(heap, merged)
    return total


def can_reach_end(jumps: list) -> bool:
    """jumps[i] = i 번 칸에서 최대 몇 칸까지 뛸 수 있는가. 마지막 칸에 닿을 수 있는지."""
    farthest = 0
    for i, jump in enumerate(jumps):
        if i > farthest:  # 여기까지 오는 길이 끊겼다
            return False
        farthest = max(farthest, i + jump)
    return True


def min_rooms(intervals: list) -> int:
    """[시작, 끝) 구간들을 모두 소화하는 데 필요한 방의 최소 개수. 끝나는 시각과 시작하는 시각이 같으면 같은 방을 쓴다."""
    ends = []  # 지금 쓰이는 방들이 끝나는 시각 (최소 힙)
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)  # 가장 일찍 끝나는 방을 재사용
        else:
            heapq.heappush(ends, end)  # 쓸 수 있는 방이 없으면 새 방
    return len(ends)


def biggest_after_removing(digits: str, k: int) -> str:
    """숫자 문자열에서 k 개를 지워 만들 수 있는 가장 큰 수(길이 len - k 인 문자열).

    앞에서부터 보며, 새 숫자가 스택의 맨 위보다 크면 위의 것을 지운다(지울 횟수가 남은 동안)."""
    stack = []
    remaining = k
    for ch in digits:
        while remaining and stack and stack[-1] < ch:
            stack.pop()
            remaining -= 1
        stack.append(ch)
    return "".join(stack[: len(stack) - remaining])


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    times = list(map(int, input().split()))[:n]
    print(min_total_wait(times))


if __name__ == "__main__":
    main()
