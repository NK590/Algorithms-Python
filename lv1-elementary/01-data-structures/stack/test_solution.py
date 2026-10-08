"""solution.py 검증: 리스트 모델과 비교 + 괄호는 "짝을 계속 지우기" 방식과 비교 + 후위 표기식은 eval 과 비교"""
import io
import random

import pytest

from tools.loader import load_solution

solution = load_solution(__file__)


def test_stack_operations_match_a_list_model():
    rng = random.Random(0)
    for _ in range(200):
        stack, model = solution.Stack(), []
        for _ in range(60):
            if model and rng.random() < 0.45:
                assert solution.Stack.peek(stack) == model[-1]
                assert stack.pop() == model.pop()
            else:
                value = rng.randint(0, 9)
                stack.push(value)
                model.append(value)
            assert len(stack) == len(model) and stack.is_empty() == (not model)


def test_empty_stack_raises():
    stack = solution.Stack()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()


def reduces_to_empty(text):
    """붙어 있는 짝 () [] {} 를 더 이상 지울 수 없을 때까지 지워서 비는지 본다 (스택을 쓰지 않는 방법)"""
    text = "".join(ch for ch in text if ch in "()[]{}")
    while True:
        shorter = text.replace("()", "").replace("[]", "").replace("{}", "")
        if shorter == text:
            return text == ""
        text = shorter


def test_is_balanced_matches_reduction():
    rng = random.Random(1)
    for _ in range(2000):
        text = "".join(rng.choice("()[]{}a") for _ in range(rng.randint(0, 10)))
        assert solution.is_balanced(text) == reduces_to_empty(text), text


def test_is_balanced_examples():
    assert solution.is_balanced("") and solution.is_balanced("(a[b]{c})")
    assert not solution.is_balanced("(]") and not solution.is_balanced("((") and not solution.is_balanced("))((")
    assert not solution.is_balanced("([)]")  # 개수는 맞지만 짝이 어긋난다


def random_expression(rng, depth):
    """(중위 표기식 문자열, 후위 토큰 리스트)"""
    if depth == 0 or rng.random() < 0.3:
        n = rng.randint(0, 9)
        return str(n), [str(n)]
    left_infix, left_post = random_expression(rng, depth - 1)
    right_infix, right_post = random_expression(rng, depth - 1)
    op = rng.choice("+-*")
    return f"({left_infix}{op}{right_infix})", left_post + right_post + [op]


def test_evaluate_postfix_matches_eval():
    rng = random.Random(2)
    for _ in range(500):
        infix, postfix = random_expression(rng, 4)
        assert solution.evaluate_postfix(postfix) == eval(infix), infix


def test_evaluate_postfix_example():
    assert solution.evaluate_postfix(["3", "4", "+", "2", "*"]) == 14
    assert solution.evaluate_postfix(["5", "1", "2", "+", "4", "*", "+", "3", "-"]) == 14
    assert solution.evaluate_postfix(["2", "7", "-"]) == -5  # 순서가 중요하다: 2 - 7


def test_reverse_with_stack():
    for text in ("", "a", "abc", "hello world"):
        assert solution.reverse_with_stack(text) == text[::-1]


def test_main(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("3\n(()\n()()\n(())\n"))
    solution.main()
    assert capsys.readouterr().out.split() == ["NO", "YES", "YES"]
