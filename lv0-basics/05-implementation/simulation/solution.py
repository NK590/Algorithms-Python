"""구현·시뮬레이션 — 문제에 적힌 규칙을 그대로 코드로 옮겨 상태를 따라가기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 알고리즘이 따로 필요한 것이 아니라, 규칙을 빠뜨리지 않고 정확히 옮기는 것이 핵심입니다.
- 직접 실행하면 `N K` 를 받아 요세푸스 순열(K번째 사람을 차례로 제거하는 순서)을 출력합니다.
"""
import sys
from collections import deque

# 북(N), 동(E), 남(S), 서(W) 순서. 오른쪽으로 돌면 인덱스 +1, 왼쪽으로 돌면 -1 이다.
FACING = "NESW"
MOVES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def simulate_robot(commands: str, rows: int, cols: int) -> tuple:
    """격자 위의 로봇을 명령대로 움직인다. 시작은 (0, 0) 에서 동쪽을 본다.

    'F' 는 보는 방향으로 한 칸 전진 (격자 밖이면 제자리), 'L' 은 왼쪽으로, 'R' 은 오른쪽으로 90도 회전.
    반환값은 (행, 열, 보는 방향).
    """
    r = c = 0
    d = 1  # 동쪽
    for command in commands:
        if command == "L":
            d = (d - 1) % 4
        elif command == "R":
            d = (d + 1) % 4
        elif command == "F":
            nr, nc = r + MOVES[d][0], c + MOVES[d][1]
            if 0 <= nr < rows and 0 <= nc < cols:  # 규칙: 벽이면 움직이지 않는다
                r, c = nr, nc
    return r, c, FACING[d]


def josephus_order(n: int, k: int) -> list:
    """1..n 번이 원으로 앉아 있고 k번째 사람을 계속 제거할 때, 제거되는 순서. 덱을 돌려 가며 그대로 시뮬레이션한다."""
    people = deque(range(1, n + 1))
    order = []
    while people:
        people.rotate(-(k - 1))  # 앞의 k-1 명을 뒤로 보내면 k번째 사람이 맨 앞에 온다
        order.append(people.popleft())
    return order


def josephus_last(n: int, k: int) -> int:
    """마지막까지 남는 사람의 번호. 시뮬레이션 없이 점화식 J(n) = (J(n-1) + k) mod n 으로 O(n)."""
    survivor = 0  # 사람이 1명일 때 그 사람의 (0부터 센) 위치
    for people in range(2, n + 1):
        survivor = (survivor + k) % people
    return survivor + 1


def add_minutes(hour: int, minute: int, delta: int) -> tuple:
    """24시간제 시계에 delta 분을 더한 (시, 분). 자정을 넘으면 0시로 돌아온다."""
    total = (hour * 60 + minute + delta) % (24 * 60)
    return total // 60, total % 60


def main() -> None:
    n, k = map(int, sys.stdin.readline().split())
    print("<" + ", ".join(map(str, josephus_order(n, k))) + ">")


if __name__ == "__main__":
    main()
