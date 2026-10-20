"""Fails the build if the docs contain real-looking contact data, scrub-list terms or broken links."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import pytest

import check_docs  # noqa: E402


def _kinds(findings):
    return [f.kind for f in findings]


def test_repo_is_clean():
    findings = check_docs.run(ROOT)
    assert findings == [], "\n" + "\n".join(str(f) for f in findings)


# Non-fictional samples are assembled at runtime so this file never matches its own scan.
REAL_PHONE = "-".join(["212", "867", "5309"])
REAL_E164 = "+1" + "212" + "867" + "5309"
REAL_EMAIL = "someone" + "@" + "gmail.com"
SAMPLE_IP = ".".join(["10", "1", "2", "3"])


def test_fictional_phone_allowed():
    assert check_docs.scan_text("x.md", "Call 212-555-0142 or +1-555-0199") == []
    assert check_docs.scan_text("x.md", "Call +12125550142") == []


def test_real_phone_flagged():
    assert "phone" in _kinds(check_docs.scan_text("x.md", f"Call {REAL_PHONE}"))
    assert "phone" in _kinds(check_docs.scan_text("x.md", f"Call {REAL_E164}"))


def test_numbers_that_are_not_phones_pass():
    text = "$97K across 963 payments; 2,873 turns; 2026-05-21 -> 2026-10-20; 9,985 customers"
    assert check_docs.scan_text("x.md", text) == []


def test_email_rules():
    assert check_docs.scan_text("x.md", "alex.rivera@example.com") == []
    assert "email" in _kinds(check_docs.scan_text("x.md", REAL_EMAIL))


def test_ipv4_flagged():
    assert "ipv4" in _kinds(check_docs.scan_text("x.md", f"host {SAMPLE_IP}"))


def test_scrub_terms_flagged():
    terms = [t for t in check_docs.SCRUB_TERMS if t[:1].isalnum() and t[-1:].isalnum()]
    if not terms:
        pytest.skip("PORTFOLIO_SCRUB_TERMS not set; private terms unavailable")
    term = terms[0]
    assert "scrub-term" in _kinds(check_docs.scan_text("x.md", f"see {term} for details"))


def test_short_name_term_uses_word_boundary():
    # A short scrub term must not match inside ordinary words such as "behavior".
    assert check_docs.scan_text("x.md", "agent behavior and aviation") == []


def test_owner_name_only_in_readme_and_license():
    if not check_docs.OWNER_NAMES:
        pytest.skip("PORTFOLIO_SCRUB_TERMS not set; owner names unavailable")
    name = check_docs.OWNER_NAMES[0] + " Example"
    assert check_docs.scan_text("README.md", name) == []
    assert check_docs.scan_text("LICENSE", name) == []
    assert "owner-name" in _kinds(check_docs.scan_text("case-studies/x.md", name))


def test_broken_relative_link_flagged(tmp_path):
    (tmp_path / "a.md").write_text("[ok](b.md) [bad](missing.md) [ext](https://example.com)")
    (tmp_path / "b.md").write_text("# b")
    findings = check_docs.check_links("a.md", (tmp_path / "a.md").read_text(), tmp_path)
    assert [f.detail for f in findings] == ["missing.md"]
