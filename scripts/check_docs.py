#!/usr/bin/env python3
"""Docs hygiene and link checker for this repository.

Checks every tracked text file for:
  * phone numbers outside the fictional 555-01xx range,
  * email addresses outside example.com,
  * IPv4 addresses,
  * scrub-list terms (private names, domains, hosts, partner identifiers),
  * the owner's full name anywhere except README.md and LICENSE,
and every Markdown file for:
  * relative links that do not resolve to a file in the repo,
  * Mermaid code fences that are empty.

Stdlib only. Exit code 0 = clean, 1 = findings. Run: python3 scripts/check_docs.py
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TEXT_SUFFIXES = {".md", ".mmd", ".sql", ".py", ".yml", ".yaml", ".toml", ".txt", ""}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}

def _load_private_terms() -> tuple[list[str], list[str], list[str]]:
    """Read private scrub terms from the file named by PORTFOLIO_SCRUB_TERMS.

    The terms live outside the repository so this public file never lists what
    it is meant to keep out. Without the variable, only the generic checks run.
    Line format: plain = forbidden term, "owner:" = name allowed only in
    README/LICENSE, "re:" = regex, "#" = comment.
    """
    path = os.environ.get("PORTFOLIO_SCRUB_TERMS", "")
    if not path or not Path(path).is_file():
        return [], [], []
    terms, owner, regexes = [], [], []
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("owner:"):
            owner.append(line[len("owner:"):])
        elif line.startswith("re:"):
            regexes.append(line[len("re:"):])
        else:
            terms.append(line)
    return terms, owner, regexes


SCRUB_TERMS, OWNER_NAMES, SCRUB_REGEXES = _load_private_terms()
# The owner's name is allowed only in the README author line and LICENSE copyright.
OWNER_NAME_ALLOWED_FILES = {"README.md", "LICENSE"}

PHONE_RE = re.compile(
    r"(?<![\w$.,])"                       # not part of a larger number, amount or identifier
    r"(?:\+?1[ .-]?)?"
    r"\(?([2-9]\d{2})\)?[ .-]"
    r"(\d{3})[ .-](\d{4})"
    r"(?![\w.,])"
)
E164_RE = re.compile(r"\+1(\d{3})(\d{3})(\d{4})\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# A deliberate public contact address is published as a mailto: link in README.md;
# any other non-example.com address, or one in another file, is a finding.
PUBLIC_CONTACT_FILES = {"README.md"}
MAILTO_RE = re.compile(r"mailto:([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
MD_LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)")
MERMAID_FENCE_RE = re.compile(r"```mermaid\n(.*?)```", re.DOTALL)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.kind}] {self.detail}"


def iter_text_files(root: Path = REPO_ROOT) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {"LICENSE", ".gitignore"}:
            files.append(path)
    return files


def _is_fictional_phone(exchange: str, line_number: str) -> bool:
    return exchange == "555" and line_number.startswith("01")


def scan_text(rel_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    is_self = rel_path == "scripts/check_docs.py"
    mailto_targets = {m.group(1).lower() for m in MAILTO_RE.finditer(text)}
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in PHONE_RE.finditer(line):
            if not _is_fictional_phone(m.group(2), m.group(3)):
                findings.append(Finding(rel_path, lineno, "phone", m.group(0).strip()))
        for m in E164_RE.finditer(line):
            if not _is_fictional_phone(m.group(2), m.group(3)):
                findings.append(Finding(rel_path, lineno, "phone", m.group(0)))
        for m in EMAIL_RE.finditer(line):
            domain = m.group(0).rsplit("@", 1)[1].lower()
            if rel_path in PUBLIC_CONTACT_FILES and m.group(0).lower() in mailto_targets:
                continue
            if domain != "example.com" and not domain.endswith(".example.com"):
                findings.append(Finding(rel_path, lineno, "email", m.group(0)))
        for m in IPV4_RE.finditer(line):
            findings.append(Finding(rel_path, lineno, "ipv4", m.group(0)))
        if is_self:
            continue
        for term in SCRUB_TERMS:
            pattern = rf"\b{re.escape(term)}\b" if term[0].isalnum() and term[-1].isalnum() else re.escape(term)
            if re.search(pattern, line, re.I):
                findings.append(Finding(rel_path, lineno, "scrub-term", "<redacted term>"))
        for regex in SCRUB_REGEXES:
            if re.search(regex, line, re.I):
                findings.append(Finding(rel_path, lineno, "scrub-term", "<redacted term>"))
        for name in OWNER_NAMES:
            if re.search(rf"\b{re.escape(name)}\b", line) and rel_path not in OWNER_NAME_ALLOWED_FILES:
                findings.append(Finding(rel_path, lineno, "owner-name", "owner name outside README/LICENSE"))
    return findings


def check_links(rel_path: str, text: str, root: Path = REPO_ROOT) -> list[Finding]:
    findings: list[Finding] = []
    base = (root / rel_path).parent
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in MD_LINK_RE.finditer(line):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (base / target_path).resolve()
            if not resolved.exists():
                findings.append(Finding(rel_path, lineno, "broken-link", target))
            elif root.resolve() not in resolved.parents and resolved != root.resolve():
                findings.append(Finding(rel_path, lineno, "link-outside-repo", target))
    for m in MERMAID_FENCE_RE.finditer(text):
        if not m.group(1).strip():
            lineno = text[: m.start()].count("\n") + 1
            findings.append(Finding(rel_path, lineno, "empty-mermaid", "empty mermaid block"))
    return findings


def run(root: Path = REPO_ROOT) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_text_files(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        findings.extend(scan_text(rel, text))
        if path.suffix == ".md":
            findings.extend(check_links(rel, text, root))
    return findings


def main() -> int:
    findings = run()
    for f in findings:
        print(f)
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
