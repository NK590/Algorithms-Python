"""solution.py 검증: 무작위 이진 트리에서 순회 결과의 성질과 복원 왕복"""
import io
import random

from tools.loader import load_solution

solution = load_solution(__file__)


def random_binary_tree(rng, n):
    """노드 0..n-1 로 이루어진 무작위 모양의 이진 트리: (tree, root)"""
    values = list(range(n))
    rng.shuffle(values)
    tree = {v: [None, None] for v in values}
    root = values[0]
    for v in values[1:]:
        node = root
        while True:  # 비어 있는 자식 자리를 찾을 때까지 무작위로 내려간다
            side = rng.randrange(2)
            if tree[node][side] is None:
                tree[node][side] = v
                break
            node = tree[node][side]
    return {k: tuple(v) for k, v in tree.items()}, root


README_TREE = {"A": ("B", "C"), "B": ("D", "E"), "C": (None, "F"), "D": (None, None), "E": (None, None), "F": (None, None)}


def test_readme_example():
    assert solution.preorder(README_TREE, "A") == list("ABDECF")
    assert solution.inorder(README_TREE, "A") == list("DBEACF")
    assert solution.postorder(README_TREE, "A") == list("DEBFCA")
    assert solution.level_order(README_TREE, "A") == list("ABCDEF")


def test_empty_tree():
    for order in (solution.preorder, solution.inorder, solution.postorder, solution.level_order):
        assert order({}, None) == []
    assert solution.inorder_iterative({}, None) == []


def test_every_node_is_visited_once_in_every_order():
    rng = random.Random(0)
    for _ in range(200):
        n = rng.randint(1, 12)
        tree, root = random_binary_tree(rng, n)
        for order in (solution.preorder, solution.inorder, solution.postorder, solution.level_order):
            assert sorted(order(tree, root)) == list(range(n))


def test_iterative_inorder_matches_recursive():
    rng = random.Random(1)
    for _ in range(200):
        tree, root = random_binary_tree(rng, rng.randint(1, 12))
        assert solution.inorder_iterative(tree, root) == solution.inorder(tree, root)


def test_orders_relate_to_each_other():
    rng = random.Random(2)
    for _ in range(200):
        tree, root = random_binary_tree(rng, rng.randint(1, 12))
        pre = solution.preorder(tree, root)
        post = solution.postorder(tree, root)
        assert pre[0] == root and post[-1] == root  # 루트는 전위의 처음, 후위의 마지막
        # 각 노드는 부모보다 전위에서 늦고 후위에서 이르다
        for parent, children in tree.items():
            for child in children:
                if child is not None:
                    assert pre.index(parent) < pre.index(child) and post.index(child) < post.index(parent)


def test_binary_search_tree_inorder_is_sorted():
    rng = random.Random(3)
    for _ in range(200):
        keys = rng.sample(range(100), rng.randint(1, 15))
        tree = {k: [None, None] for k in keys}
        root = keys[0]
        for key in keys[1:]:
            node = root
            while True:
                side = 0 if key < node else 1
                if tree[node][side] is None:
                    tree[node][side] = key
                    break
                node = tree[node][side]
        tree = {k: tuple(v) for k, v in tree.items()}
        assert solution.inorder(tree, root) == sorted(keys)


def test_rebuild_from_preorder_and_inorder():
    rng = random.Random(4)
    for _ in range(300):
        tree, root = random_binary_tree(rng, rng.randint(1, 12))
        rebuilt, rebuilt_root = solution.build_from_preorder_inorder(
            solution.preorder(tree, root), solution.inorder(tree, root))
        assert rebuilt_root == root and rebuilt == tree


def test_rebuild_from_postorder_and_inorder():
    rng = random.Random(5)
    for _ in range(300):
        tree, root = random_binary_tree(rng, rng.randint(1, 12))
        rebuilt, rebuilt_root = solution.build_from_postorder_inorder(
            solution.postorder(tree, root), solution.inorder(tree, root))
        assert rebuilt_root == root and rebuilt == tree


def test_main(monkeypatch, capsys):
    text = "6\nA B C\nB D E\nC . F\nD . .\nE . .\nF . .\n"
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    solution.main()
    assert capsys.readouterr().out.split() == ["ABDECF", "DBEACF", "DEBFCA"]
