#!/usr/bin/env python3
"""문서의 외부 URL 응답을 확인한다. 접근 제한은 삭제된 링크와 구분한다."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import urllib.error
import urllib.request
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
URL_RE = re.compile(r"\]\((https?://[^\s)]+)\)")


@dataclass
class Result:
    url: str
    outcome: str
    status: int | None = None
    detail: str = ""


def collect_urls(root: Path) -> list[str]:
    urls = set()
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        if any(part.startswith(".") for part in relative.parts) or relative.parts[:2] == ("docs", "TEMPLATE"):
            continue
        urls.update(URL_RE.findall(path.read_text(encoding="utf-8")))
    return sorted(urls)


def check_url(url: str, timeout: float = 15) -> Result:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return Result(url, "broken", detail="invalid URL")
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        return Result(url, "broken", detail="invalid URL")
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": "Algorithms-Python link checker"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return Result(url, "ok", response.status)
        except urllib.error.HTTPError as error:
            if error.code in (405, 501) and method == "HEAD":
                continue
            if error.code in (404, 410):
                return Result(url, "broken", error.code, "page not found")
            return Result(url, "unverified", error.code, "access limited or temporary server response")
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            return Result(url, "unverified", detail=str(error))
    return Result(url, "unverified", detail="unsupported request method")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=15, help="one request timeout in seconds")
    parser.add_argument("--workers", type=int, default=4, help="maximum concurrent requests")
    parser.add_argument("--report", type=Path, help="optional JSON result file")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or args.workers < 1:
        parser.error("timeout and workers must be positive")
    urls = collect_urls(ROOT)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda url: check_url(url, args.timeout), urls))
    counts = {outcome: sum(result.outcome == outcome for result in results)
              for outcome in ("ok", "broken", "unverified")}
    for result in results:
        if result.outcome != "ok":
            print(f"{result.outcome}: {result.url} ({result.status or result.detail})")
    print(json.dumps({"checked": len(results), **counts}, ensure_ascii=False))
    if args.report:
        args.report.write_text(json.dumps({"summary": counts, "results": [asdict(r) for r in results]},
                                         ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not results:
        return 2
    return 1 if counts["broken"] else 2 if counts["unverified"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
