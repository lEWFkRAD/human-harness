"""Small, dependency-free publication hygiene check; not a secret scanner."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__", ".venv", ".pytest_cache"}
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".txt", ".example"}
PATTERNS = {
    "absolute user path": re.compile(r"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]", re.I),
    "absolute unix home": re.compile(r"/(?:home|Users)/[A-Za-z0-9_.-]+/"),
    "private tailnet domain": re.compile(r"[A-Za-z0-9.-]+\.ts\.net", re.I),
    "private IPv4 address": re.compile(r"\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2})\b"),
    "possible access token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{24,})\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".pyc", ".pyo", ".jsonl", ".tip", ".lock"}


def main() -> int:
    problems = []
    files_checked = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append((rel, "runtime/private artifact"))
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore", ".gitattributes"}:
            continue
        files_checked += 1
        content = path.read_text(encoding="utf-8")
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                problems.append((rel, label))
    if problems:
        for rel, label in problems:
            print(f"FAIL {rel}: {label}")
        return 1
    print(f"PASS: {files_checked} public text files checked; no configured privacy patterns found.")
    print("This check is not comprehensive and is not a production-safety assertion.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
