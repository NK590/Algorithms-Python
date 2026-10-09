from pathlib import Path

import pytest

from tools import gen_index as gi


# ---------------------------------------------------------------- 파서

def test_front_matter_parses_scalars_and_lists():
    text = "---\nlevel: 2\ntags: [graph, shortest-path]\nprerequisites: []\ntime: O((V+E) log V)\n---\n# 제목\n"
    meta, body = gi.parse_front_matter(text)
    assert meta == {"level": "2", "tags": ["graph", "shortest-path"], "prerequisites": [], "time": "O((V+E) log V)"}
    assert body == "# 제목\n"


def test_front_matter_value_may_contain_commas_and_colons():
    meta, _ = gi.parse_front_matter("---\ntime: 평균 O(n log n), 최악 O(n^2)\nsummary: 목표: 풀기\n---\n")
    assert meta["time"] == "평균 O(n log n), 최악 O(n^2)"
    assert meta["summary"] == "목표: 풀기"


def test_front_matter_absent():
    assert gi.parse_front_matter("# 제목\n") == ({}, "# 제목\n")


def test_front_matter_rejects_line_without_colon():
    with pytest.raises(ValueError):
        gi.parse_front_matter("---\nbroken line\n---\n")


def test_first_h1_ignores_code_fences():
    assert gi.first_h1("```\n# not a title\n```\n# 진짜 제목\n") == "진짜 제목"


def test_replace_block_only_touches_marked_region():
    text = "앞\n<!-- INDEX:START -->\n낡은 내용\n<!-- INDEX:END -->\n뒤\n"
    assert gi.replace_block(text, "INDEX", "새 내용") == "앞\n<!-- INDEX:START -->\n새 내용\n<!-- INDEX:END -->\n뒤\n"


def test_replace_block_requires_markers():
    with pytest.raises(KeyError):
        gi.replace_block("마커 없음", "INDEX", "x")


# ---------------------------------------------------------------- 검증 (임시 리포지토리)

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo(tmp_path: Path, **overrides) -> Path:
    """레벨 1개 / 그룹 1개 / 개념 2개(a, b: a 가 선행)짜리 최소 리포지토리"""
    write(tmp_path / "lv0-basics" / "README.md",
          "---\nlevel: 0\nname: 입문\ntier: Bronze\nsummary: 요약\n---\n# Lv0\n<!-- INDEX:START -->\n<!-- INDEX:END -->\n")
    write(tmp_path / "lv0-basics" / "01-group" / "README.md", "# 그룹\n")
    for slug, pre in (("a", "[]"), ("b", "[a]")):
        pre = overrides.get(f"pre_{slug}", pre)
        write(tmp_path / "lv0-basics" / "01-group" / slug / "README.md",
              f"---\nlevel: 0\ntags: [t]\nprerequisites: {pre}\nstatus: {overrides.get('status', 'stub')}\n---\n# {slug.upper()}\n")
        write(tmp_path / "lv0-basics" / "01-group" / slug / "solution.py", "")
    return tmp_path


def test_valid_minimal_repo(tmp_path):
    repo = gi.load_repo(make_repo(tmp_path))
    assert repo.errors == []
    assert list(repo.concepts()) == ["a", "b"]


def test_concepts_are_sorted_by_order_then_name(tmp_path):
    root = make_repo(tmp_path)
    group = root / "lv0-basics" / "01-group"
    for slug, order in (("a", 2), ("b", 1)):
        readme = group / slug / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("level: 0\n", f"level: 0\norder: {order}\n"), encoding="utf-8")
    repo = gi.load_repo(root)
    assert repo.errors == []
    assert [c.slug for c in repo.levels[0].concepts] == ["b", "a"]


def test_invalid_order_is_reported(tmp_path):
    root = make_repo(tmp_path)
    readme = root / "lv0-basics" / "01-group" / "a" / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("level: 0\n", "level: 0\norder: first\n"), encoding="utf-8")
    assert any("order" in e for e in gi.load_repo(root).errors)


def test_graph_has_nodes_edges_and_level_colors(tmp_path):
    graph = gi.render_graph(gi.load_repo(make_repo(tmp_path)))
    assert graph.startswith("```mermaid\nflowchart LR")
    assert 'n_a["a"]' in graph and 'n_b["b"]' in graph
    assert "n_a --> n_b" in graph
    assert "class n_a,n_b lv0" in graph
    assert graph.endswith("색상: Lv0 초록")


def test_unknown_prerequisite_is_reported(tmp_path):
    repo = gi.load_repo(make_repo(tmp_path, pre_b="[nope]"))
    assert any("'nope'" in e for e in repo.errors)


def test_prerequisite_cycle_is_reported(tmp_path):
    repo = gi.load_repo(make_repo(tmp_path, pre_a="[b]"))
    assert any("사이클" in e for e in repo.errors)


def test_done_requires_tests_and_problems(tmp_path):
    repo = gi.load_repo(make_repo(tmp_path, status="done"))
    assert any("test_solution.py" in e for e in repo.errors)
    assert any("problems.md" in e for e in repo.errors)


def test_invalid_status_is_reported(tmp_path):
    repo = gi.load_repo(make_repo(tmp_path, status="wip"))
    assert any("status" in e for e in repo.errors)


def test_missing_solution_is_reported(tmp_path):
    root = make_repo(tmp_path)
    (root / "lv0-basics" / "01-group" / "a" / "solution.py").unlink()
    assert any("solution.py" in e for e in gi.load_repo(root).errors)


def test_broken_relative_link_is_reported(tmp_path):
    root = make_repo(tmp_path)
    write(root / "docs.md", "[있음](lv0-basics/README.md) [없음](nope.md) [외부](https://example.com) `[코드](x.md)`\n")
    repo = gi.load_repo(root)
    gi.check_links(repo)
    broken = [e for e in repo.errors if "깨진 링크" in e]
    assert len(broken) == 1 and "nope.md" in broken[0]


def completed_concept(tmp_path):
    path = tmp_path / "concept"
    write(path / "test_solution.py", "def test_example():\n    assert 2 + 2 == 4\n")
    write(path / "problems.md", "\n".join(
        f"| {i} | [problem](https://example.com/{i}) | 핵심 연습 | 상태와 전이를 확인한다 |"
        for i in range(1, 4)))
    body = "\n".join(f"## {i}. 설명\n본문" for i in range(1, 10))
    for heading in gi.EXPLANATION_HEADINGS:
        # Inline expressions are meaningful explanation content; fenced code is not.
        body += f"\n### {heading}\n`dist[v] = min(dist[v], dist[u] + weight)`로 더 짧은 경로를 반영한다.\n"
    return path, {"time": "O(n)", "space": "O(n)"}, body


def test_done_accepts_real_tests_and_explanation_with_inline_expressions(tmp_path):
    path, meta, body = completed_concept(tmp_path)
    repo = gi.Repo(tmp_path)
    gi.validate_done_content(repo, path, meta, body)
    assert repo.errors == []


def test_done_rejects_empty_tests_and_duplicate_or_unexplained_problems(tmp_path):
    path, meta, body = completed_concept(tmp_path)
    write(path / "test_solution.py", "# Tests will be added later.\n")
    write(path / "problems.md", "\n".join([
        "| 1 | [a](https://example.com/a) | 핵심 연습 | 설명 |",
        "| 2 | [a again](https://example.com/a) | 핵심 연습 | 설명 |",
        "| 3 | [b](https://example.com/b) | 핵심 연습 | |",
        "| 4 | [c](https://example.com/c) | 핵심 연습 | |",
    ]))
    repo = gi.Repo(tmp_path)
    gi.validate_done_content(repo, path, meta, body)
    assert any("실제 테스트 함수" in error for error in repo.errors)
    assert any("문제 링크를 3개" in error for error in repo.errors)


def test_done_rejects_missing_complexity_and_heading_only_explanations(tmp_path):
    path, meta, body = completed_concept(tmp_path)
    del meta["space"]
    body = "\n".join(f"### {heading}" for heading in gi.EXPLANATION_HEADINGS)
    body += "\n```python\n## 1. This is code, not a section\n```\n"
    repo = gi.Repo(tmp_path)
    gi.validate_done_content(repo, path, meta, body)
    assert any("space" in error for error in repo.errors)
    assert sum("구체적으로" in error for error in repo.errors) == 3
    assert sum("번 섹션" in error for error in repo.errors) == 9


def test_done_reports_test_file_syntax_error(tmp_path):
    path, meta, body = completed_concept(tmp_path)
    write(path / "test_solution.py", "def test_broken(:\n")
    repo = gi.Repo(tmp_path)
    gi.validate_done_content(repo, path, meta, body)
    assert any("구문 오류" in error for error in repo.errors)


def test_markdown_anchors_support_unicode_duplicates_and_html_but_ignore_fences():
    text = """# 한글 `Code`!
# 한글 Code!
# 한글 Code-1
<a id="explicit"></a>
~~~html
# hidden
<span id="also-hidden"></span>
~~~
"""
    assert gi.markdown_anchors(text) == {"한글-code", "한글-code-1", "한글-code-1-1", "explicit"}


def test_link_check_reports_missing_fragments_and_accepts_percent_encoded_anchors(tmp_path):
    root = make_repo(tmp_path)
    write(root / "docs.md", "# 한글 제목\n[a](#%ED%95%9C%EA%B8%80-%EC%A0%9C%EB%AA%A9)\n[b](#missing)\n")
    write(root / "other.md", "[valid](docs.md#한글-제목)\n[bad](docs.md#nope)\n")
    repo = gi.load_repo(root)
    gi.check_links(repo)
    assert len(repo.errors) == 2
    assert all("없는 문서 앵커" in error for error in repo.errors)


@pytest.mark.parametrize("url", ["https:///missing-host", "https://user:pass@example.com/", "https://[invalid/"])
def test_invalid_external_urls_are_reported(tmp_path, url):
    root = make_repo(tmp_path)
    write(root / "docs.md", f"[problem]({url})\n")
    repo = gi.load_repo(root)
    gi.check_links(repo)
    assert len(repo.errors) == 1 and "잘못된 외부 URL" in repo.errors[0]


def test_replaced_problem_platform_is_rejected(tmp_path):
    root = make_repo(tmp_path)
    write(root / "docs.md", "[old problem](https://www.acmicpc.net/problem/1000)\n")
    repo = gi.load_repo(root)
    gi.check_links(repo)
    assert any("교체가 필요한 문제 레퍼런스" in error for error in repo.errors)


# ---------------------------------------------------------------- 실제 리포지토리

def test_repository_structure_and_links_are_valid():
    repo = gi.load_repo()
    gi.check_links(repo)
    assert repo.errors == []


def test_generated_sections_are_up_to_date():
    repo = gi.load_repo()
    outputs = gi.build_outputs(repo)
    assert repo.errors == []
    stale = [repo.rel(p) for p, text in outputs.items() if gi.read_text(p) != text]
    assert stale == [], "`python tools/gen_index.py` 를 실행해 자동 생성 구간을 갱신하세요"
