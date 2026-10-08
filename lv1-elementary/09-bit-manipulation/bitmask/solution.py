"""비트마스크 — 작은 집합을 정수 하나로 표현하고, 집합 연산을 비트 연산으로 하기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 원소 k 가 집합에 있으면 k 번째 비트가 1. 원소가 n 개면 집합은 0 ~ 2ⁿ-1 의 정수 하나이고 그 정수가 곧 "상태"다.
- 모든 부분집합을 0 .. 2ⁿ-1 로 돌 수 있어서 브루트포스와 비트마스크 DP 의 기본 틀이 된다.
- 직접 실행하면 `M` 과 M 개의 명령(add/remove/check/toggle/all/empty)을 받아, 원소 1..20 의 집합에 적용하고 check 의 결과를 출력합니다.
"""
import sys


def from_elements(elements: list) -> int:
    """원소 목록(0 부터 센다)을 마스크로."""
    mask = 0
    for k in elements:
        mask |= 1 << k
    return mask


def to_elements(mask: int) -> list:
    """마스크를 원소 목록(오름차순)으로."""
    elements = []
    k = 0
    while mask >> k:
        if mask >> k & 1:
            elements.append(k)
        k += 1
    return elements


def full_mask(n: int) -> int:
    """원소 0..n-1 을 모두 가진 집합."""
    return (1 << n) - 1


def add(mask: int, k: int) -> int:
    return mask | (1 << k)


def remove(mask: int, k: int) -> int:
    return mask & ~(1 << k)


def contains(mask: int, k: int) -> bool:
    return bool(mask >> k & 1)


def toggle(mask: int, k: int) -> int:
    return mask ^ (1 << k)


def size(mask: int) -> int:
    """원소의 수 = 켜진 비트의 수."""
    count = 0
    while mask:
        mask &= mask - 1
        count += 1
    return count


def complement(mask: int, n: int) -> int:
    """전체 집합(0..n-1)에서의 여집합. ~mask 는 음수가 되므로 full_mask 와 XOR 한다."""
    return mask ^ full_mask(n)


def submasks(mask: int) -> list:
    """mask 의 모든 부분집합(공집합 포함)을 큰 것부터 반환한다.

    sub 에서 1 을 빼면 가장 낮은 켜진 비트가 꺼지고 그 아래가 모두 켜지는데, & mask 로 mask 밖의 비트를 지우면 다음으로 작은 부분집합이 된다.
    부분집합의 수 = 2^size(mask) 이므로 모든 mask 의 부분집합을 합치면 3ⁿ."""
    result = []
    sub = mask
    while True:
        result.append(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask
    return result


def masks_with_k_bits(n: int, k: int) -> list:
    """n 비트 중 정확히 k 비트가 켜진 모든 마스크를 오름차순으로 (고스퍼의 해킹). 조합 C(n, k) 개.

    다음 마스크 = 가장 낮은 연속한 1 묶음의 맨 위 1 을 한 칸 올리고, 나머지 1 들은 맨 아래로 내린다."""
    if k == 0:
        return [0]
    result = []
    mask = (1 << k) - 1
    limit = 1 << n
    while mask < limit:
        result.append(mask)
        lowest = mask & -mask
        ripple = mask + lowest
        mask = (((ripple ^ mask) >> 2) // lowest) | ripple
    return result


def count_subsets_with_sum(numbers: list, target: int) -> int:
    """합이 target 인 비어 있지 않은 부분집합의 수. 2ⁿ 개의 마스크를 모두 확인한다 (n ≤ 20 안팎)."""
    n = len(numbers)
    count = 0
    for mask in range(1, 1 << n):
        total = 0
        for i in range(n):
            if mask >> i & 1:
                total += numbers[i]
        if total == target:
            count += 1
    return count


def min_team_difference(synergy: list) -> int:
    """n 명(짝수)을 n/2 명씩 두 팀으로 나눌 때, 두 팀 능력치의 차이의 최솟값.

    synergy[i][j] = i 와 j 가 같은 팀일 때 더해지는 값(대칭이 아닐 수 있다). 팀의 능력치 = 팀 안의 모든 순서쌍 (i, j) 의 합."""
    n = len(synergy)
    full = full_mask(n)
    best = None
    for mask in masks_with_k_bits(n, n // 2):
        if mask & 1 == 0:  # 0 번이 있는 쪽을 팀 A 로 고정해 대칭인 반쪽을 건너뛴다
            continue
        a = [i for i in range(n) if mask >> i & 1]
        b = [i for i in range(n) if not mask >> i & 1]
        score_a = sum(synergy[i][j] for i in a for j in a if i != j)
        score_b = sum(synergy[i][j] for i in b for j in b if i != j)
        diff = abs(score_a - score_b)
        best = diff if best is None else min(best, diff)
    return 0 if best is None else best


def process_commands(commands: list) -> list:
    """원소 1..20 의 집합에 명령을 적용하고 check 의 결과(1/0)를 모은다.

    명령: "add x", "remove x", "check x", "toggle x", "all", "empty"."""
    mask = 0
    results = []
    for command in commands:
        parts = command.split()
        op = parts[0]
        if op == "all":
            mask = full_mask(21) & ~1  # 1..20
        elif op == "empty":
            mask = 0
        else:
            x = int(parts[1])
            if op == "add":
                mask = add(mask, x)
            elif op == "remove":
                mask = remove(mask, x)
            elif op == "check":
                results.append(1 if contains(mask, x) else 0)
            elif op == "toggle":
                mask = toggle(mask, x)
    return results


def main() -> None:
    input = sys.stdin.readline
    m = int(input())
    commands = [input().strip() for _ in range(m)]
    print("\n".join(map(str, process_commands(commands))))


if __name__ == "__main__":
    main()
