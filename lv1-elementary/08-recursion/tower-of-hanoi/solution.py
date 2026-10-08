"""하노이의 탑 — 재귀로 큰 문제를 "더 작은 같은 문제 + 한 번의 이동"으로 쪼개기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- n 개의 원판을 A → C 로 옮기려면: ① 위의 n-1 개를 B 로 ② 가장 큰 원판을 C 로 ③ B 의 n-1 개를 C 로.
- 이동 횟수는 T(n) = 2·T(n-1) + 1 = 2ⁿ - 1 로, 최소임이 증명됩니다. 출력 자체가 2ⁿ - 1 줄이라 n 이 커지면 모두 출력할 수 없습니다.
- 직접 실행하면 `N` 을 받아 이동 횟수와 (N ≤ 20 이면) 이동 순서를 출력합니다.
"""
import sys


def hanoi_moves_detailed(n: int, source: int = 1, spare: int = 2, target: int = 3) -> list:
    """(원판 번호, 출발 기둥, 도착 기둥) 목록. 원판은 작은 것부터 1, 2, …, n."""
    moves = []

    def move(k, src, mid, dst):
        if k == 0:
            return
        move(k - 1, src, dst, mid)  # 위의 k-1 개를 보조 기둥으로 치운다
        moves.append((k, src, dst))  # 가장 큰 원판(k)을 목표로
        move(k - 1, mid, src, dst)  # 치워 둔 k-1 개를 그 위로 옮긴다

    move(n, source, spare, target)
    return moves


def hanoi_moves(n: int, source: int = 1, spare: int = 2, target: int = 3) -> list:
    """(출발 기둥, 도착 기둥) 목록. 길이는 2ⁿ - 1."""
    return [(src, dst) for _, src, dst in hanoi_moves_detailed(n, source, spare, target)]


def hanoi_count(n: int) -> int:
    """최소 이동 횟수 2ⁿ - 1. 점화식 T(n) = 2·T(n-1) + 1, T(0) = 0 을 풀면 나온다."""
    return (1 << n) - 1


def hanoi_count_recursive(n: int) -> int:
    """점화식을 그대로 코드로 옮긴 것. (이동을 만들지 않고 횟수만 센다)"""
    return 0 if n == 0 else 2 * hanoi_count_recursive(n - 1) + 1


def hanoi_kth_move(n: int, k: int, source: int = 1, spare: int = 2, target: int = 3) -> tuple:
    """전체 이동을 만들지 않고 k 번째(1 부터) 이동을 O(n) 에 구한다. 반환값은 (원판, 출발, 도착).

    가운데(2^(n-1) 번째) 이동이 가장 큰 원판이고, 그 앞은 (n-1) 개짜리 앞 단계, 뒤는 뒷 단계다."""
    half = 1 << (n - 1)
    if k == half:
        return (n, source, target)
    if k < half:
        return hanoi_kth_move(n - 1, k, source, target, spare)
    return hanoi_kth_move(n - 1, k - half, spare, source, target)


def disk_moved_at(k: int) -> int:
    """k 번째 이동(1 부터)에서 옮기는 원판 번호. k 를 이진수로 썼을 때 끝의 0 의 개수 + 1.

    1 2 1 3 1 2 1 4 … (눈금자 수열): 가장 작은 원판은 홀수 번째마다, 두 번째 원판은 4 로 나눈 나머지가 2 일 때마다 움직인다."""
    return (k & -k).bit_length()


def hanoi_iterative(n: int) -> list:
    """재귀 없이 같은 이동을 만든다. 번갈아 ① 가장 작은 원판을 정해진 방향으로 한 칸 ② 작은 원판이 아닌 쪽에서 가능한 유일한 이동.

    가장 작은 원판의 방향은 n 이 홀수면 1→3→2→1, 짝수면 1→2→3→1 순서다."""
    pegs = {1: list(range(n, 0, -1)), 2: [], 3: []}
    order = [1, 3, 2] if n % 2 == 1 else [1, 2, 3]
    moves = []
    smallest_at = 0  # order 안에서 가장 작은 원판이 있는 위치
    for step in range(1, hanoi_count(n) + 1):
        if step % 2 == 1:
            src = order[smallest_at]
            smallest_at = (smallest_at + 1) % 3
            dst = order[smallest_at]
        else:
            a, b = [p for p in (1, 2, 3) if p != order[smallest_at]]
            # 작은 원판이 없는 두 기둥 사이에서 더 작은 맨 위 원판이 큰 쪽으로 간다 (빈 기둥에는 무엇이든 올라간다)
            if not pegs[a] or (pegs[b] and pegs[b][-1] < pegs[a][-1]):
                src, dst = b, a
            else:
                src, dst = a, b
        pegs[dst].append(pegs[src].pop())
        moves.append((src, dst))
    return moves


def main() -> None:
    n = int(sys.stdin.readline())
    out = [str(hanoi_count(n))]
    if n <= 20:
        out.extend(f"{a} {b}" for a, b in hanoi_moves(n))
    print("\n".join(out))


if __name__ == "__main__":
    main()
