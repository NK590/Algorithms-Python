### Union-Find (유니온 파인드, Disjoint Set - 서로소 집합)

# 상호 배타적으로 이루어진(=교집합이 없는) 집합을 관리하는 트리 형태의 자료 구조
# 서로 다른 두 집합을 병합하는 Union 연산, 특정 원소가 어떤 집합에 속해있는지 판단하는 Find 연산을 지원

### 예시 코드

# 각 원소의 부모 원소를 나타내는 리스트. 인덱스가 그 원소의 번호, 리스트값이 그 원소의 부모 번호
# 초기값을 자기 자신으로 설정해 루트로 만듬
parent = [i for i in range(10)]

# find 연산
def find(target):
    # 루트일 시 자기 자신을 출력
    if target == parent[target]:
        return target
    
    # 메모이제이션을 이용하여 경로 최적화
    parent[target] = find(parent[target])
    return parent[target]

# union 연산
def union(a, b):
    a = find(a)
    b = find(b)
    
    # 작은 루트 노드를 기준으로 합침
    if a < b:
        parent[b] = a
    else:
        parent[a] = b