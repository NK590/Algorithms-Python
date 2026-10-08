### Tower of Hanoi (하노이의 탑)
# 세 개의 장대가 있고 첫 번째 장대에는 반경이 서로 다른 n개의 원판이 쌓여 있다.
# 각 원판은 반경이 큰 순서대로 쌓여있다. 
# 이제 수도승들이 다음 규칙에 따라 첫 번째 장대에서 세 번째 장대로 옮기려 한다.

# 한 번에 한 개의 원판만을 다른 탑으로 옮길 수 있다.
# 쌓아 놓은 원판은 항상 위의 것이 아래의 것보다 작아야 한다.
# 이 작업을 수행하는데 필요한 이동 순서를 출력하는 프로그램을 작성하라. 
# 단, 이동 횟수는 최소가 되어야 한다.

### 예시 코드
# 일반적으로 재귀를 이용한 분할 정복으로 풀이함

import sys

# n : 원판의 개수
# first, second, third : 순서대로 첫번째, 두번째, 세번째 장대
def hanoi(n, first, second, third):
    # 원판이 하나 남은 경우, 첫번째에서 세번째로 옮김
    if n == 1:
        print(first, third)
    else:
        # 제일 큰 원판을 남기고 나머지를 옮기기까지 과정
        hanoi(n-1, first, third, second)
        # 제일 큰 원판 옮기기
        print(first, third)
        # 나머지 원판들을 다시 제일 큰 원판 위에 돌려놓기
        hanoi(n-1, second, first, third)

n = int(sys.stdin.readline())

hanoi(n, 1, 2, 3)