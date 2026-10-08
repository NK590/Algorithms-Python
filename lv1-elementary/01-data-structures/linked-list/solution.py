### Linked List (연결 리스트)

# 메모리의 있는 데이터를 물리적으로 연속된 공간을 사용하지 않고, 특정 데이터가 그 다음 데이터를 가르키도록
# 다음 데이터의 위치를 포함시켜서 세트로 입/출력을 받는 자료 구조
# 임의의 위치에 데이터를 입/출력을 받을 때 O(1)의 시간복잡도를 가져서 매우 효율적이지만,
# 임의의 위치의 데이터를 참조할 때는 배열 등과 다르게 처음부터 데이터를 순차적으로 참조해야 될 필요가 있어
# 시간복잡도가 O(n)으로 비효율적임

# 데이터의 참조 순서를 단방향으로 정의하는 단일 연결 리스트, 쌍방향으로 정의하는 이중 연결 리스트,
# 시작 데이터와 끝 데이터 사이를 참조 가능하게 이어붙인 순환 연결 리스트 등이 있음

# C와 같은 언어에서는 포인터를 이용하여 비교적 쉽게 구현이 가능하지만, Python에서는 구현이 다소 까다로움

### 예시 코드
# 여기서는 단일 연결 리스트를 구현함

class Node:
    def __init__(self, data):
        self.data = data
        # 초기값의 다음 값의 초기값은 None
        self.next = None

class Linked_List:
    def __init__(self, data):
        self.head = Node(data)
    
    # 헤더부터 탐색해 뒤에 새로운 노드 추가하기
    def append(self, data):
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = Node(data)
    
    # 모든 노드 값 출력
    def print_all(self):
        cur = self.head
        while cur is not None:
            print(cur.data)
            cur = cur.next
    
    # 노드 인덱스 알아내기
    def get_node(self, index):
        count = 0
        node = self.head
        while count < index:
            count += 1
            node = node.next
        return node
    
    # 노드 삽입
    def add_node(self, index, value):
        new_node = Node(value)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
            return
        node = self.get_node(index - 1)
        next_node = node.next
        node.next = new_node
        new_node.next = next_node
    
    # 노드 삭제
    def delete_node(self, index):
        if index == 0:
            self.head = self.head.next
            return
        node = self.get_node(index - 1)
        node.next = node.next.next
        
### 예제
# 위에서 정의한 연결리스트 클래스로 정의한 인스턴스
LL = Linked_List(0)

LL.print_all()

LL.append(1)
LL.append(2)
LL.append(4)
LL.print_all()

LL.add_node(1, 10)
LL.print_all()

LL.delete_node(3)
LL.print_all()