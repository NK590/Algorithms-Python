### Quick Sort (퀵 소트)

# 특정 축(Pivot)을 설정하여 그 축을 기준으로 축 앞쪽에서 축보다 큰 갚은 축 뒤로,
# 축 뒤쪽에서 축보다 작은 값은 축 뒤쪽으로 보내는 걸 반복해서 정렬하는 알고리즘.
# 이름에서 알 수 있듯이 평균적으로 빠른 정렬 알고리즘(O(nlogn))으로, 많은 언어에서 
# 자체 제공하는 정렬 함수에서 사용하는 알고리즘임

### 예시 코드 1

def Quick_Sort(li: list):
    # li의 크기가 1이 될 때까지 재귀 선언
    if len(li) < 2:
        return li
    
    # 편의상 축(pivot)을 입력된 리스트 길이의 절반으로 선언
    pivot = len(li) // 2
    front_li = []
    pivot_li = []
    back_li = []
    
    # 입력 리스트의 각 값을 축과 비교해서, 각각 맞는 리스트로 원소를 집어넣음
    for value in li:
        if value < li[pivot]:
            front_li.append(value)
        elif value > li[pivot]:
            back_li.append(value)
        else:
            pivot_li.append(value)
    
    return Quick_Sort(front_li) + Quick_Sort(pivot_li) + Quick_Sort(back_li)

### 예시 코드 2
# 파이썬의 List Comprehension을 이용하여 보다 직관적이고 간단한 구현

def Quick_Sort_2(li: list):
    if len(li) < 2:
        return li
    
    # 축을 편의상 0번째 원소로 하고, 나머지는 tail 리스트로 선언
    pivot = li[0]
    tail = li[1:]
    
    # List Comprehension으로 축을 기점으로 tail 리스트 원소를 비교해서 두 리스트로 분리
    left = [x for x in tail if x <= pivot]
    right = [x for x in tail if x > pivot]
    
    return Quick_Sort_2(left) + [pivot] + Quick_Sort_2(right)

### 예시 코드 3
# 위 두 예시는 정렬 과정에서 지속적으로 리스트를 선언하여 메모리를 소모하므로,
# 새로운 리스트를 선언하지 않고 입력 리스트의 원소 스왑만을 이용하여 구현하는 방법

def Quick_Sort_3(li: list, li_start: int, li_end: int):
    # 입력 리스트 원소가 1개인 경우 무시함
    if li_start >= li_end:
        return
    # 축을 첫 번째 원소로 설정
    pivot = li_start
    left = li_start + 1
    right = li_end
    
    while left <= right:
        # 축보다 큰 데이터를 찾을 떄까지 left를 증가
        while left <= li_end and li[left] <= li[pivot]:
            left += 1
        # 축보다 작은 데이터를 찾을 때까지 right를 감소
        while right > li_start and li[right] >= li[pivot]:
            right -= 1
        # left와 right가 엇갈렸다면 작은 데이터와 축을 교체
        if left > right:
            li[right], li[pivot] = li[pivot], li[right]
        # 엇갈리지 않았다면 작은 데이터와 큰 데이터를 교체
        else:
            li[right], li[left] = li[left], li[right]
    # 위 일련의 과정을 right를 기준으로 분할하여 재귀적으로 반복
    Quick_Sort_3(li, li_start, right - 1)
    Quick_Sort_3(li, right + 1, li_end)

### 예제

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
ans = Quick_Sort(li)
print("after :", ans)

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
ans = Quick_Sort_2(li)
print("after :", ans)

li = [1, 9, 2, 3, 7, 4, 5, 0, 6, 8]
print("before :", li)
Quick_Sort_3(li, 0, len(li)-1)
print("after :", li)