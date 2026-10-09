#!/usr/bin/env python3
"""리포지토리 구조 검증 + 목차 자동 생성 도구 (표준 라이브러리만 사용)

    python tools/gen_index.py           # README.md / lvN-*/README.md / ROADMAP.md 의 자동 생성 구간을 갱신
    python tools/gen_index.py --check   # 구조·링크 검증 + 자동 생성 구간이 최신인지 확인 (CI용)

자동 생성 구간은 아래 마커 사이에 들어가며, 마커 바깥은 사람이 쓴 내용이라 건드리지 않는다.

    <!-- INDEX:START -->  ...  <!-- INDEX:END -->     (루트/레벨 README: 개념 표)
    <!-- GRAPH:START -->  ...  <!-- GRAPH:END -->     (ROADMAP: 선행 관계 mermaid 그래프)

디렉터리 규칙
    lvN-<이름>/README.md                  레벨 설명 (front matter: level, name, tier, summary)
    lvN-<이름>/NN-<그룹>/README.md        토픽 그룹 설명 (H1이 그룹 제목)
    lvN-<이름>/NN-<그룹>/<개념>/          개념 하나 (README.md + solution.py [+ test_solution.py + problems.md])
"""
from __future__ import annotations

import argparse
import ast
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

# 개념 문서의 진행 상태
STATUSES = {
    "stub": "개념 설명만 있고 구현 코드는 없음",
    "migrated": "기존 코드·설명을 옮겨 둔 상태 (문서 템플릿 미적용)",
    "draft": "문서 템플릿에 맞춰 작성 중",
    "done": "설명·구현·테스트·연습문제를 모두 갖춤",
}
CONCEPT_KEYS = {"level", "order", "tags", "prerequisites", "time", "space", "status"}
LEVEL_KEYS = {"level", "name", "tier", "summary"}

LEVEL_RE = re.compile(r"^lv(\d+)-[a-z0-9]+(-[a-z0-9]+)*$")
GROUP_RE = re.compile(r"^\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.S)
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
EXPLANATION_HEADINGS = (
    "무엇을 저장하고 어떻게 움직이나",
    "왜 이 방법이 맞는가",
    "작은 예제로 검산하기",
)


# ---------------------------------------------------------------- 파싱

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def parse_value(raw: str):
    """'[a, b]' 는 리스트, 따옴표는 벗기고, 나머지는 문자열 그대로"""
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip() for item in raw[1:-1].split(",") if item.strip()]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_front_matter(text: str) -> tuple[dict, str]:
    """`---` 로 둘러싼 단순 `key: value` front matter 를 (dict, 본문) 으로 분리"""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"front matter 줄에 ':' 가 없습니다: {line!r}")
        meta[key.strip()] = parse_value(value.strip())
    return meta, text[match.end():]


def first_h1(body: str) -> str | None:
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith("# "):
            return line[2:].strip()
    return None


# ---------------------------------------------------------------- 모델

@dataclass
class Concept:
    slug: str
    level: int
    group: str
    path: Path
    title: str
    meta: dict

    @property
    def status(self) -> str:
        return self.meta["status"]


@dataclass
class Group:
    name: str
    path: Path
    title: str
    concepts: list[Concept] = field(default_factory=list)


@dataclass
class Level:
    number: int
    path: Path
    meta: dict
    groups: list[Group] = field(default_factory=list)

    @property
    def concepts(self) -> list[Concept]:
        return [c for g in self.groups for c in g.concepts]


@dataclass
class Repo:
    root: Path
    levels: list[Level] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def concepts(self) -> dict[str, Concept]:
        return {c.slug: c for lv in self.levels for c in lv.concepts}

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()


def concept_sort_key(concept: Concept) -> tuple[int, str]:
    """그룹 안에서는 front matter 의 order 순(없으면 맨 뒤), 같으면 이름순"""
    order = str(concept.meta.get("order", ""))
    return (int(order) if order.isdigit() else 10**6, concept.slug)


def subdirs(path: Path) -> list[Path]:
    return sorted(p for p in path.iterdir()
                  if p.is_dir() and not p.name.startswith((".", "_")))


# ---------------------------------------------------------------- 로드 + 검증

def load_doc(repo: Repo, path: Path, required: bool = True) -> tuple[dict, str] | None:
    if not path.is_file():
        if required:
            repo.errors.append(f"{repo.rel(path)}: 파일이 없습니다")
        return None
    try:
        return parse_front_matter(read_text(path))
    except ValueError as e:
        repo.errors.append(f"{repo.rel(path)}: {e}")
        return None


def unknown_keys(repo: Repo, path: Path, meta: dict, allowed: set[str]) -> None:
    for key in sorted(set(meta) - allowed):
        repo.errors.append(f"{repo.rel(path)}: 알 수 없는 front matter 키 '{key}' (허용: {', '.join(sorted(allowed))})")


def load_concept(repo: Repo, lv: Level, group: Group, path: Path) -> None:
    rel = repo.rel(path)
    if not SLUG_RE.match(path.name):
        repo.errors.append(f"{rel}: 개념 폴더 이름은 kebab-case 영문이어야 합니다")
        return
    doc = load_doc(repo, path / "README.md")
    if doc is None:
        return
    meta, body = doc
    readme = repo.rel(path / "README.md")
    unknown_keys(repo, path / "README.md", meta, CONCEPT_KEYS)

    if str(meta.get("level")) != str(lv.number):
        repo.errors.append(f"{readme}: level 이 폴더의 레벨({lv.number})과 다릅니다 (현재: {meta.get('level')!r})")
    if not isinstance(meta.get("tags"), list) or not meta["tags"]:
        repo.errors.append(f"{readme}: tags 는 비어 있지 않은 리스트여야 합니다 (예: tags: [graph, bfs])")
    if not isinstance(meta.get("prerequisites"), list):
        repo.errors.append(f"{readme}: prerequisites 는 리스트여야 합니다 (없으면 'prerequisites: []')")
    if "order" in meta and not (str(meta["order"]).isdigit() and int(meta["order"]) >= 1):
        repo.errors.append(f"{readme}: order 는 1 이상의 정수여야 합니다 (현재: {meta['order']!r})")
    if meta.get("status") not in STATUSES:
        repo.errors.append(f"{readme}: status 는 {', '.join(STATUSES)} 중 하나여야 합니다 (현재: {meta.get('status')!r})")
    title = first_h1(body)
    if not title:
        repo.errors.append(f"{readme}: H1 제목('# ...')이 없습니다")
    if not (path / "solution.py").is_file():
        repo.errors.append(f"{rel}: solution.py 가 없습니다")
    if meta.get("status") == "done":
        for name in ("test_solution.py", "problems.md"):
            if not (path / name).is_file():
                repo.errors.append(f"{rel}: status 가 done 이면 {name} 이 필요합니다")
        validate_done_content(repo, path, meta, body)

    group.concepts.append(Concept(path.name, lv.number, group.name, path, title or path.name, meta))


def validate_done_content(repo: Repo, path: Path, meta: dict, body: str) -> None:
    """완료 표시가 빈 파일이나 제목만으로 통과하지 않도록 최소 내용을 검사한다."""
    rel = repo.rel(path)
    for key in ("time", "space"):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            repo.errors.append(f"{rel}/README.md: done 개념에는 {key} 복잡도 설명이 필요합니다")
    prose = strip_fenced_code(body)
    for number in range(1, 10):
        if not re.search(rf"^## {number}\.\s+\S", prose, flags=re.M):
            repo.errors.append(f"{rel}/README.md: done 개념에는 {number}번 섹션이 필요합니다")
    for heading in EXPLANATION_HEADINGS:
        match = re.search(rf"^### {re.escape(heading)}\s*\n(.*?)(?=^#|\Z)", prose, flags=re.M | re.S)
        if not match or len(match[1].strip()) < 40:
            repo.errors.append(f"{rel}/README.md: '{heading}' 설명을 구체적으로 작성하세요")
    tests = path / "test_solution.py"
    if tests.is_file():
        try:
            tree = ast.parse(read_text(tests), filename=str(tests))
            if not any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                       and node.name.startswith("test_") for node in ast.walk(tree)):
                repo.errors.append(f"{rel}/test_solution.py: 실제 테스트 함수가 없습니다")
        except SyntaxError as error:
            repo.errors.append(f"{rel}/test_solution.py: 구문 오류: {error.msg}")
    problems = path / "problems.md"
    if problems.is_file():
        rows = re.findall(r"^\|\s*\d+\s*\|.*$", read_text(problems), flags=re.M)
        urls = set()
        for row in rows:
            columns = re.split(r"(?<!\\)\|", row)[1:-1]
            if len(columns) == 4 and all(column.strip() for column in columns):
                urls.update(target for target in LINK_RE.findall(columns[1]) if target.startswith("https://"))
        if len(urls) < 3:
            repo.errors.append(f"{rel}/problems.md: 학습 포인트가 있는 서로 다른 HTTPS 문제 링크를 3개 이상 작성하세요")


def load_group(repo: Repo, lv: Level, path: Path) -> None:
    rel = repo.rel(path)
    if not GROUP_RE.match(path.name):
        repo.errors.append(f"{rel}: 그룹 폴더 이름은 'NN-kebab-case' 형식이어야 합니다")
        return
    doc = load_doc(repo, path / "README.md")
    title = first_h1(doc[1]) if doc else None
    if doc and not title:
        repo.errors.append(f"{rel}/README.md: H1 제목('# ...')이 없습니다")
    group = Group(path.name, path, title or path.name)
    lv.groups.append(group)
    for concept_dir in subdirs(path):
        load_concept(repo, lv, group, concept_dir)
    if not group.concepts:
        repo.errors.append(f"{rel}: 개념 폴더가 하나도 없습니다")
    group.concepts.sort(key=concept_sort_key)


def load_level(repo: Repo, path: Path) -> None:
    number = int(LEVEL_RE.match(path.name).group(1))
    doc = load_doc(repo, path / "README.md")
    meta = doc[0] if doc else {}
    readme = repo.rel(path / "README.md")
    if doc:
        unknown_keys(repo, path / "README.md", meta, LEVEL_KEYS)
        for key in sorted(LEVEL_KEYS - set(meta)):
            repo.errors.append(f"{readme}: front matter 에 '{key}' 가 없습니다")
        if "level" in meta and str(meta["level"]) != str(number):
            repo.errors.append(f"{readme}: level 이 폴더 번호({number})와 다릅니다 (현재: {meta['level']!r})")
    lv = Level(number, path, meta)
    repo.levels.append(lv)
    for group_dir in subdirs(path):
        load_group(repo, lv, group_dir)


def validate_prerequisites(repo: Repo) -> None:
    concepts = repo.concepts()
    seen: dict[str, Concept] = {}
    for lv in repo.levels:
        for c in lv.concepts:
            if c.slug in seen:
                repo.errors.append(f"{repo.rel(c.path)}: 개념 이름 '{c.slug}' 이 {repo.rel(seen[c.slug].path)} 와 중복됩니다")
            seen[c.slug] = c

    graph: dict[str, list[str]] = {}
    for c in concepts.values():
        pre = c.meta.get("prerequisites")
        if not isinstance(pre, list):
            continue
        graph[c.slug] = []
        for p in pre:
            readme = repo.rel(c.path / "README.md")
            if p == c.slug:
                repo.errors.append(f"{readme}: 자기 자신을 선행 개념으로 지정할 수 없습니다")
            elif p not in concepts:
                repo.errors.append(f"{readme}: 선행 개념 '{p}' 이(가) 존재하지 않습니다")
            elif concepts[p].level > c.level:
                repo.errors.append(f"{readme}: 선행 개념 '{p}'(Lv{concepts[p].level})이 더 높은 레벨입니다")
            else:
                graph[c.slug].append(p)

    # 사이클 검사 (DFS 색칠)
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                cycle = " -> ".join(stack[stack.index(nxt):] + [nxt]) if nxt in stack else f"{node} -> {nxt}"
                repo.errors.append(f"선행 관계에 사이클이 있습니다: {cycle}")
            elif nxt not in state:
                visit(nxt, stack + [nxt])
        state[node] = 2

    for slug in graph:
        if slug not in state:
            visit(slug, [slug])


def load_repo(root: Path = ROOT) -> Repo:
    repo = Repo(root)
    for path in sorted(p for p in root.iterdir() if p.is_dir()):
        if LEVEL_RE.match(path.name):
            load_level(repo, path)
    repo.levels.sort(key=lambda lv: lv.number)
    if not repo.levels:
        repo.errors.append("lvN-* 레벨 폴더가 없습니다")
    validate_prerequisites(repo)
    return repo


# ---------------------------------------------------------------- 링크 검사

def strip_fenced_code(text: str) -> str:
    return re.sub(r"^```.*?^```|^~~~.*?^~~~", "", text, flags=re.S | re.M)


def strip_code(text: str) -> str:
    return re.sub(r"`[^`\n]*`", "", strip_fenced_code(text))


def markdown_anchors(text: str) -> set[str]:
    """GitHub의 일반적인 제목 앵커와 명시적 HTML 앵커를 수집한다."""
    without_fences = strip_fenced_code(text)
    anchors = set(re.findall(r'<(?:a|span)\s+[^>]*(?:id|name)=[\"\']([^\"\']+)', without_fences, flags=re.I))
    counts: dict[str, int] = {}
    heading_anchors: set[str] = set()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", without_fences, flags=re.M):
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading).lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        duplicate = counts.get(slug, 0)
        candidate = f"{slug}-{duplicate}" if duplicate else slug
        while candidate in heading_anchors:
            duplicate += 1
            candidate = f"{slug}-{duplicate}"
        counts[slug] = duplicate + 1
        heading_anchors.add(candidate)
    anchors.update(heading_anchors)
    return anchors


def check_links(repo: Repo) -> None:
    """상대 파일·문서 앵커·외부 URL 형식을 검사한다. 외부 접속은 별도 도구가 맡는다."""
    template = (repo.root / "docs" / "TEMPLATE").resolve()
    anchor_cache: dict[Path, set[str]] = {}
    for dirpath, dirnames, filenames in os.walk(repo.root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix != ".md" or template in path.resolve().parents:
                continue
            for target in LINK_RE.findall(strip_code(read_text(path))):
                if SCHEME_RE.match(target):
                    try:
                        parsed = urlsplit(target)
                    except ValueError:
                        repo.errors.append(f"{repo.rel(path)}: 잘못된 외부 URL → {target}")
                        continue
                    if parsed.scheme in ("http", "https"):
                        if not parsed.hostname or parsed.username or parsed.password:
                            repo.errors.append(f"{repo.rel(path)}: 잘못된 외부 URL → {target}")
                        elif parsed.hostname == "acmicpc.net" or parsed.hostname.endswith(".acmicpc.net"):
                            repo.errors.append(f"{repo.rel(path)}: 교체가 필요한 문제 레퍼런스 → {target}")
                    continue
                file_part, _, fragment = target.partition("#")
                destination = (path.parent / unquote(file_part)).resolve() if file_part else path.resolve()
                if not destination.exists():
                    repo.errors.append(f"{repo.rel(path)}: 깨진 링크 → {target}")
                elif fragment and destination.is_file() and destination.suffix == ".md":
                    if destination not in anchor_cache:
                        anchor_cache[destination] = markdown_anchors(read_text(destination))
                    if unquote(fragment) not in anchor_cache[destination]:
                        repo.errors.append(f"{repo.rel(path)}: 없는 문서 앵커 → {target}")


# ---------------------------------------------------------------- 생성

def md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def link(from_dir: Path, to: Path, text: str) -> str:
    rel = Path(os.path.relpath(to, from_dir)).as_posix()
    return f"[{text}]({rel}/)"


def render_root_index(repo: Repo) -> str:
    statuses = list(STATUSES)
    lines = ["| 레벨 | 이름 | 난이도 표기 | 개념 | " + " | ".join(f"`{s}`" for s in statuses) + " | 목표 |",
             "|---|---|---|---:|" + "---:|" * len(statuses) + "---|"]
    for lv in repo.levels:
        concepts = lv.concepts
        counts = [str(sum(c.status == s for c in concepts)) for s in statuses]
        meta = lv.meta
        lines.append(
            f"| {link(repo.root, lv.path, f'Lv{lv.number}')} | {meta.get('name', '')} | {meta.get('tier', '')} "
            f"| {len(concepts)} | " + " | ".join(counts) + f" | {md_escape(str(meta.get('summary', '')))} |")
    return "\n".join(lines)


def render_level_index(repo: Repo, lv: Level) -> str:
    if not lv.groups:
        return "아직 추가된 개념이 없습니다. 예정된 주제는 [ROADMAP](../ROADMAP.md)을 참고하세요."
    concepts = repo.concepts()
    blocks = []
    for group in lv.groups:
        rows = [f"### {link(lv.path, group.path, group.title)}", "",
                "| 개념 | 상태 | 시간 복잡도 | 선행 개념 |", "|---|---|---|---|"]
        for c in group.concepts:
            pre = [link(lv.path, concepts[p].path, p) for p in c.meta.get("prerequisites", []) if p in concepts]
            rows.append(f"| {link(lv.path, c.path, md_escape(c.title))} | `{c.status}` "
                        f"| {md_escape(str(c.meta.get('time', '-')))} | {', '.join(pre) or '-'} |")
        blocks.append("\n".join(rows))
    return "\n\n".join(blocks)


LEVEL_COLORS = [("초록", "#d8f0d8"), ("파랑", "#d6e6fb"), ("노랑", "#fdf0c4"),
                ("주황", "#fbd9c8"), ("보라", "#f2d0ee"), ("회색", "#e0e0e0")]


def render_graph(repo: Repo) -> str:
    """선행 관계 mermaid 그래프 (서브그래프 없이 레벨별 색상으로 구분해야 층이 깔끔하게 나뉜다)"""
    def node(slug: str) -> str:
        return "n_" + slug.replace("-", "_")

    concepts = list(repo.concepts().values())
    lines = ["```mermaid", "flowchart LR"]
    lines += [f'  {node(c.slug)}["{c.slug}"]' for c in concepts]
    lines += [f"  {node(p)} --> {node(c.slug)}" for c in concepts for p in c.meta.get("prerequisites", [])]
    legend = []
    for lv in repo.levels:
        if not lv.concepts:
            continue
        color_name, color = LEVEL_COLORS[lv.number % len(LEVEL_COLORS)]
        lines.append(f"  classDef lv{lv.number} fill:{color},stroke:#555,color:#111")
        lines.append(f"  class {','.join(node(c.slug) for c in lv.concepts)} lv{lv.number}")
        legend.append(f"Lv{lv.number} {color_name}")
    lines.append("```")
    return "\n".join(lines) + f"\n\n색상: {' · '.join(legend)}"


def replace_block(text: str, name: str, content: str) -> str:
    start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if not pattern.search(text):
        raise KeyError(f"{start} ... {end} 마커가 없습니다")
    return pattern.sub(lambda _: f"{start}\n{content}\n{end}", text, count=1)


def build_outputs(repo: Repo) -> dict[Path, str]:
    """자동 생성 구간을 채운 새 파일 내용을 {경로: 내용} 으로 계산"""
    jobs = [(repo.root / "README.md", "INDEX", render_root_index(repo)),
            (repo.root / "ROADMAP.md", "GRAPH", render_graph(repo))]
    jobs += [(lv.path / "README.md", "INDEX", render_level_index(repo, lv)) for lv in repo.levels]
    outputs = {}
    for path, marker, content in jobs:
        try:
            outputs[path] = replace_block(read_text(path), marker, content)
        except FileNotFoundError:
            repo.errors.append(f"{repo.rel(path)}: 파일이 없습니다")
        except KeyError as e:
            repo.errors.append(f"{repo.rel(path)}: {e.args[0]}")
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="구조 검증 + 목차 자동 생성")
    parser.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검증만 한다 (최신이 아니면 실패)")
    args = parser.parse_args(argv)

    repo = load_repo()
    check_links(repo)
    outputs = build_outputs(repo)
    if repo.errors:
        print(f"검증 실패 ({len(repo.errors)}건)", file=sys.stderr)
        for error in repo.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    stale = [p for p, text in outputs.items() if read_text(p) != text]
    if args.check:
        if stale:
            print("자동 생성 구간이 최신이 아닙니다. `python tools/gen_index.py` 를 실행해 커밋하세요:", file=sys.stderr)
            for path in stale:
                print(f"  - {repo.rel(path)}", file=sys.stderr)
            return 1
        print(f"OK: 레벨 {len(repo.levels)}개, 개념 {len(repo.concepts())}개")
        return 0

    for path in stale:
        path.write_text(outputs[path], encoding="utf-8", newline="\n")
        print(f"갱신: {repo.rel(path)}")
    if not stale:
        print("변경 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
