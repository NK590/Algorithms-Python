### Selection Sort (선택 정렬)

# 인접한 원소들끼리만 비교해서 교환하는 버블 정렬과 다르게 처음부터 끝까지 한번 훑은 다음,
# 제일 작은 원소를 맨 앞으로 보내는 것을 반복하는 알고리즘
# 버블 정렬과 비슷하게 시간 복잡도는 O(n^2)로 비효율적

### 예시 코드

def Selection_Sort(li: list):
    n = len(li)
    for i in range(len(li)):
        # i+1번째 인덱스부터 반복문을 돌려서 min_index에 제일 작은 값의 인덱스를 갱신
        min_index = i
        for j in range(i + 1, n):
            if li[j] < li[min_index]:
                min_index = j
        # i번째 인덱스 자료값과 min_index 값을 바꿔서 제일 작은 값을 앞으로 보냄
        li[i], li[min_index] = li[min_index], li[i]
    return li

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
Selection_Sort(li)
print("after :", li)
