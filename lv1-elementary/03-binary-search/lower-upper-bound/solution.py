"""lower bound / upper bound — 정렬된 배열에서 "x 이상이 처음 나오는 위치"와 "x 초과가 처음 나오는 위치"

README.md 의 설명과 짝을 이루는 참고 구현입니다.
- 둘 다 `partition_point` (조건이 False…False True…True 로 바뀌는 첫 위치 찾기)의 특수한 경우입니다. 파이썬의 bisect_left, bisect_right 와 같습니다.
- 직접 실행하면 `N`, 정렬된 N 개의 수, `M`, M 개의 질문을 받아 각 질문의 수가 배열에 몇 개 있는지 출력합니다.
"""
import sys


def partition_point(lo: int, hi: int, predicate) -> int:
    """[lo, hi) 에서 predicate(i) 가 False 가 이어지다가 True 가 이어진다고 할 때, 처음 True 인 i. 모두 False 이면 hi."""
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid  # mid 도 답의 후보이므로 버리지 않는다
        else:
            lo = mid + 1
    return lo


def lower_bound(arr: list, x) -> int:
    """arr[i] >= x 인 첫 위치. 그런 값이 없으면 len(arr). x 를 넣어도 정렬이 유지되는 가장 왼쪽 위치이기도 하다."""
    return partition_point(0, len(arr), lambda i: arr[i] >= x)


def upper_bound(arr: list, x) -> int:
    """arr[i] > x 인 첫 위치. 없으면 len(arr). x 를 넣어도 정렬이 유지되는 가장 오른쪽 위치이기도 하다."""
    return partition_point(0, len(arr), lambda i: arr[i] > x)


def count_equal(arr: list, x) -> int:
    """x 와 같은 원소의 개수. 같은 값은 연속해 있으므로 [lower_bound, upper_bound) 구간의 길이다."""
    return upper_bound(arr, x) - lower_bound(arr, x)


def count_in_range(arr: list, low, high) -> int:
    """low <= 값 <= high 인 원소의 개수."""
    return upper_bound(arr, high) - lower_bound(arr, low)


def floor_value(arr: list, x):
    """x 이하인 가장 큰 원소. 없으면 None."""
    i = upper_bound(arr, x)
    return arr[i - 1] if i > 0 else None


def ceil_value(arr: list, x):
    """x 이상인 가장 작은 원소. 없으면 None."""
    i = lower_bound(arr, x)
    return arr[i] if i < len(arr) else None


def main() -> None:
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))[:n]
    m = int(input())
    queries = list(map(int, input().split()))[:m]
    print(*(count_equal(arr, q) for q in queries))


if __name__ == "__main__":
    main()
