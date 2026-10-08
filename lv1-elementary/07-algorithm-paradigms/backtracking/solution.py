"""백트래킹 — 선택을 하나씩 쌓아 가다가, 답이 될 수 없다고 판단되면 바로 되돌아가기

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 틀: 선택한다 → 재귀로 다음 단계 → 선택을 취소한다. 조건에 어긋나는 가지는 들어가기 전에 자른다(가지치기).
- 직접 실행하면 `N` 을 받아 N 개의 퀸을 서로 공격하지 못하게 놓는 경우의 수를 출력합니다.
"""
import sys


def pick_permutations(n: int, m: int) -> list:
    """1..n 에서 중복 없이 m 개를 고른 수열을 사전 순으로 모두 반환한다. (순서가 의미 있다)"""
    result = []
    chosen = []
    used = [False] * (n + 1)

    def dfs():
        if len(chosen) == m:
            result.append(tuple(chosen))
            return
        for x in range(1, n + 1):
            if not used[x]:
                used[x] = True
                chosen.append(x)  # 선택한다
                dfs()  # 다음 자리를 채운다
                chosen.pop()  # 선택을 취소한다
                used[x] = False

    dfs()
    return result


def pick_combinations(n: int, m: int) -> list:
    """1..n 에서 m 개를 고른 오름차순 수열을 사전 순으로 모두 반환한다. (순서가 의미 없다)

    다음 숫자를 항상 방금 고른 수보다 크게만 고르면 같은 조합이 순서만 바뀌어 중복되지 않는다."""
    result = []
    chosen = []

    def dfs(start):
        if len(chosen) == m:
            result.append(tuple(chosen))
            return
        # 남은 자리를 채울 만큼의 숫자가 남아 있어야 한다 (가지치기)
        for x in range(start, n - (m - len(chosen)) + 2):
            chosen.append(x)
            dfs(x + 1)
            chosen.pop()

    dfs(1)
    return result


def all_subsets(items: list) -> list:
    """모든 부분집합 (공집합 포함). 각 원소를 넣는다 / 넣지 않는다 두 갈래로 나뉜다."""
    result = []
    chosen = []

    def dfs(i):
        if i == len(items):
            result.append(list(chosen))
            return
        dfs(i + 1)  # i 번째를 넣지 않는다
        chosen.append(items[i])
        dfs(i + 1)  # i 번째를 넣는다
        chosen.pop()

    dfs(0)
    return result


def n_queens_count(n: int) -> int:
    """N×N 체스판에 퀸 N 개를 서로 공격하지 못하게 놓는 경우의 수.

    행마다 하나씩 놓는다. 같은 열(cols), 같은 / 대각선(row + col), 같은 \\ 대각선(row - col)은 집합으로 O(1) 에 검사한다."""
    cols, diag1, diag2 = set(), set(), set()

    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue  # 공격받는 칸은 들어가지 않는다 (가지치기)
            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            count += place(row + 1)
            cols.remove(col)
            diag1.remove(row + col)
            diag2.remove(row - col)
        return count

    return place(0)


def n_queens_first(n: int):
    """퀸을 놓는 방법 하나를 사전 순으로 가장 앞선 것으로 반환한다. 없으면 None. 반환값[row] = 그 행에 놓은 열."""
    cols, diag1, diag2 = set(), set(), set()
    placement = []

    def place(row):
        if row == n:
            return True
        for col in range(n):
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue
            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            placement.append(col)
            if place(row + 1):
                return True  # 하나만 찾으면 되므로 바로 끝낸다 (취소하지 않는다)
            placement.pop()
            cols.remove(col)
            diag1.remove(row + col)
            diag2.remove(row - col)
        return False

    return list(placement) if place(0) else None


def n_queens_nodes(n: int) -> int:
    """백트래킹이 방문한 상태(놓는 시도를 통과한 칸)의 수. 가지치기가 얼마나 줄이는지 보려고 센다."""
    cols, diag1, diag2 = set(), set(), set()
    visited = 0

    def place(row):
        nonlocal visited
        if row == n:
            return
        for col in range(n):
            if col in cols or (row + col) in diag1 or (row - col) in diag2:
                continue
            visited += 1
            cols.add(col)
            diag1.add(row + col)
            diag2.add(row - col)
            place(row + 1)
            cols.remove(col)
            diag1.remove(row + col)
            diag2.remove(row - col)

    place(0)
    return visited


def generate_parentheses(n: int) -> list:
    """올바른 괄호 문자열 중 길이가 2n 인 것을 사전 순('(' < ')')으로 모두 반환한다. 개수는 카탈란 수."""
    result = []
    chars = []

    def dfs(opened, closed):
        if len(chars) == 2 * n:
            result.append("".join(chars))
            return
        if opened < n:  # 여는 괄호는 n 개까지
            chars.append("(")
            dfs(opened + 1, closed)
            chars.pop()
        if closed < opened:  # 닫는 괄호는 열린 것보다 많아질 수 없다 (가지치기)
            chars.append(")")
            dfs(opened, closed + 1)
            chars.pop()

    dfs(0, 0)
    return result


def solve_sudoku(grid: list):
    """9×9 스도쿠(빈 칸은 0)를 풀어 새 격자를 반환한다. 풀 수 없으면 None. 입력은 바꾸지 않는다.

    후보가 가장 적은 빈 칸부터 채우면 막다른 길을 일찍 발견한다."""
    board = [row[:] for row in grid]
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == 0:
                empties.append((r, c))
            else:
                b = r // 3 * 3 + c // 3
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    return None  # 처음부터 규칙에 어긋난다
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)

    def candidates(r, c):
        return [v for v in range(1, 10) if v not in rows[r] and v not in cols[c] and v not in boxes[r // 3 * 3 + c // 3]]

    def solve(remaining):
        if not remaining:
            return True
        best = min(range(len(remaining)), key=lambda i: len(candidates(*remaining[i])))
        remaining[best], remaining[-1] = remaining[-1], remaining[best]
        r, c = remaining.pop()
        b = r // 3 * 3 + c // 3
        for v in candidates(r, c):
            board[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if solve(remaining):
                return True
            rows[r].remove(v)
            cols[c].remove(v)
            boxes[b].remove(v)
        remaining.append((r, c))
        remaining[best], remaining[-1] = remaining[-1], remaining[best]
        return False

    return board if solve(empties) else None


def main() -> None:
    n = int(sys.stdin.readline())
    print(n_queens_count(n))


if __name__ == "__main__":
    main()
