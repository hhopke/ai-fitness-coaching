#!/usr/bin/env python3
"""Lint the rules layer and the data-ownership rule.

Checks:
  1. RULES.md YAML blocks parse; rule ids are unique.
  2. Every rule carries source: or judgment_call:.
  3. Activation tags resolve to a discipline, state or dossier field named in
     DOSSIER.template.md (and dossier:<field>=<value> to a listed value).
  4. DOSSIER.template.md names only existing rules, and its per-field rule
     lists match the activation tags in RULES.md.
  5. confidence: is present and uses only the allowed labels;
     "N/A (architectural)" and source_label: only with judgment_call:.
  6. RULES.md version is bumped whenever rule content changed against --base.
  7. Capabilities: every requires: entry is defined in capabilities.md;
     each capability is well formed, uses only the known providers, has a
     manual prompt if manual supplies it, and is required by some rule
     unless display_only. RULES.md names no MCP tool. Capabilities no
     provider supplies are listed as warnings, with the rules needing them.
  8. Data ownership: tracked files outside reviews/ contain no platform-owned
     values (CLAUDE.md, data ownership). Cited literature figures are
     allowlisted in tools/lint_allowlist.txt.

Usage: python tools/lint_rules.py [--base <git ref>]
Exit status 1 on any error. Requires PyYAML.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "RULES.md"
TEMPLATE = ROOT / "DOSSIER.template.md"
CAPABILITIES = ROOT / "capabilities.md"
PROVIDERS = {"intervals-icu", "manual"}
ALLOWLIST = ROOT / "tools" / "lint_allowlist.txt"

ALLOWED_LABELS = {"CONSENSUS", "CONTESTED", "PRACTITIONER", "NO EVIDENCE"}
# Rules that make no evidential claim. Valid only with judgment_call:.
ARCHITECTURAL = "N/A (architectural)"
STATES = {"rehab"}
TYPES = {"HARD", "SOFT", "BRANCH", "DISCLOSURE"}

# Platform-owned values (CLAUDE.md, data ownership). Relative figures such as
# "95-105% FTP" are not values and are not matched.
OWNERSHIP_PATTERNS = {
    "athlete id": r"\bi\d{4,8}\b",
    "power": r"(?<![\d.])\d{2,4}(?:\.\d+)?\s?(?:W|watts?)\b(?!')",
    "power/kg": r"(?<![\d.])\d(?:\.\d+)?\s?W/kg\b",
    "heart rate": r"(?<![\d.])\d{2,3}\s?bpm\b",
    "pace": r"(?<![\d.:])\d{1,2}:\d{2}\s?(?:min)?/(?:km|mi|100\s?m)\b",
    "metric assignment": (
        r"\b(?:e?FTP|CP|W'|LTHR|FTHR|max\s?HR|resting\s?HR|RHR|CSS|HRV|"
        r"CTL|ATL|TSB|ramp)\s*[:=]\s*\d"
    ),
}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def parse_rules(text: str, where: str) -> list[dict]:
    rules: list[dict] = []
    for i, block in enumerate(re.findall(r"```yaml\n(.*?)```", text, re.S)):
        try:
            loaded = yaml.safe_load(block)
        except yaml.YAMLError as e:
            err(f"{where}: YAML block {i + 1} does not parse: {e}")
            continue
        if not isinstance(loaded, list):
            err(f"{where}: YAML block {i + 1} is not a list of rules")
            continue
        rules += loaded
    return rules


def parse_template(text: str) -> tuple[set[str], dict[str, str]]:
    """Return (disciplines, {dossier field key: section text})."""
    m = re.search(r"from: ((?:`[a-z]+`,?\s*)+)", text)
    disciplines = set(re.findall(r"`([a-z]+)`", m.group(1))) if m else set()
    if not disciplines:
        err("DOSSIER.template.md: discipline list ('from: `a`, `b`') not found")
    fields: dict[str, str] = {}
    sections = re.split(r"^## ", text, flags=re.M)
    for sec in sections:
        h = re.match(r".*? — `([a-z_]+)`\s*$", sec.splitlines()[0]) if sec else None
        if h:
            fields[h.group(1)] = sec
    return disciplines, fields


def activation_terms(act: str) -> list[tuple[str, str, str | None]]:
    """Return (kind, name, value) for each tag in an activation expression."""
    terms = []
    for kind, name, value in re.findall(
        r"\b(discipline|state|dossier):([a-z_]+)(?:=([a-z_]+))?", act
    ):
        terms.append((kind, name, value or None))
    rest = re.sub(r"\b(?:discipline|state|dossier):[a-z_]+(?:=[a-z_]+)?", "", act)
    rest = re.sub(r"\bwithin \d+d\b|\bbefore load increase\b", "", rest)
    rest = re.sub(r"\b(?:AND|OR|NOT|always|dormant)\b", "", rest)
    if rest.strip(" ()"):
        terms.append(("unknown", rest.strip(), None))
    return terms


def check_rules(rules: list[dict], disciplines: set[str], fields: dict[str, str]) -> None:
    ids = [r.get("id") for r in rules]
    for i in {i for i in ids if ids.count(i) > 1}:
        err(f"RULES.md: duplicate id {i}")
    for r in rules:
        rid = r.get("id", "<no id>")
        if not re.fullmatch(r"[a-z0-9_]+", str(rid)):
            err(f"{rid}: id is not snake_case")
        if "source" not in r and "judgment_call" not in r:
            err(f"{rid}: neither source: nor judgment_call:")
        if r.get("type") not in TYPES:
            err(f"{rid}: type {r.get('type')!r} not in {sorted(TYPES)}")
        if "contradicted_by" in r:
            err(f"{rid}: unresolved contradicted_by:")
        conf = r.get("confidence")
        if conf is None:
            err(f"{rid}: confidence: missing")
        elif str(conf).strip() == ARCHITECTURAL:
            if "judgment_call" not in r:
                err(f"{rid}: confidence {ARCHITECTURAL!r} requires judgment_call:")
        else:
            conf = str(conf)
            if "N/A" in conf:
                err(f"{rid}: confidence must be exactly {ARCHITECTURAL!r} when architectural")
            found = {lab for lab in ALLOWED_LABELS if lab in conf}
            stray = set(re.findall(r"\b[A-Z]{4,}(?: [A-Z]{4,})?\b", conf)) - ALLOWED_LABELS
            stray -= {w for lab in found for w in lab.split()}
            if not found:
                err(f"{rid}: confidence {conf!r} uses none of {sorted(ALLOWED_LABELS)}")
            for s in sorted(stray):
                err(f"{rid}: confidence uses unknown label {s!r}")
        if "source_label" in r and "judgment_call" not in r:
            err(f"{rid}: source_label: requires judgment_call: explaining the mapping")
        act = r.get("activation")
        if not act:
            err(f"{rid}: activation: missing")
            continue
        if act == "dormant" and "reason" not in r:
            err(f"{rid}: dormant without reason:")
        for kind, name, value in activation_terms(str(act)):
            if kind == "unknown":
                err(f"{rid}: activation has unresolved text {name!r}")
            elif kind == "discipline" and name not in disciplines:
                err(f"{rid}: discipline:{name} is not a discipline in DOSSIER.template.md")
            elif kind == "state" and name not in STATES:
                err(f"{rid}: state:{name} is not a known state {sorted(STATES)}")
            elif kind == "dossier":
                if name not in fields:
                    err(f"{rid}: dossier:{name} is not a field in DOSSIER.template.md")
                elif value and f"`{value}`" not in fields[name]:
                    err(f"{rid}: dossier:{name}={value} is not a value listed for {name}")
        for f in set(re.findall(r"\b(\d\d-[a-z-]+\.md)\b", str(r.get("source", "")))):
            if not (ROOT / "reviews" / f).exists():
                err(f"{rid}: source cites missing file reviews/{f}")


def check_template_lists(rules: list[dict], disciplines: set[str], fields: dict[str, str], text: str) -> None:
    by_id = {r["id"]: r for r in rules if "id" in r}
    named = set(re.findall(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`", text))
    keys = set(fields) | {"rehab_case"} | set(re.findall(r"Section name: `([a-z_]+)`", text))
    tools = {n for n in named if n.startswith("icu_")}
    for n in sorted(named - set(by_id) - keys - tools):
        err(f"DOSSIER.template.md: names unknown rule {n}")

    def positive(act: str, tag: str) -> bool:
        return re.search(rf"(?<!NOT ){re.escape(tag)}\b", act) is not None

    # Disciplines: each bullet "- **<name>** — ..." names exactly its rules,
    # except combination rules, which may be named under either discipline.
    disc_sec = fields.get("disciplines", "")
    bullets = dict(re.findall(r"^- \*\*([a-z]+)\*\* — (.*?)(?=^- \*\*|^\S|\Z)", disc_sec, re.S | re.M))
    for d in sorted(disciplines):
        if d not in bullets:
            err(f"DOSSIER.template.md: no rule list for discipline {d}")
    for d, body in bullets.items():
        for rid in re.findall(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`", body):
            if rid in by_id and not positive(by_id[rid]["activation"], f"discipline:{d}"):
                if rid != "strength_dose_target":  # named as always-on, not as activated
                    err(f"DOSSIER.template.md: {rid} listed under {d} but not activated by discipline:{d}")
    for r in rules:
        for d in disciplines:
            if positive(r["activation"], f"discipline:{d}"):
                homes = [x for x in disciplines if positive(r["activation"], f"discipline:{x}")]
                if not any(f"`{r['id']}`" in bullets.get(h, "") for h in homes):
                    err(f"DOSSIER.template.md: {r['id']} (discipline:{d}) not listed under {' or '.join(homes)}")
    # Dossier fields: every rule gated on a field is named in that field's section.
    for key, sec in fields.items():
        if key == "disciplines":
            continue
        for r in rules:
            if re.search(rf"\bdossier:{key}\b", r["activation"]) and f"`{r['id']}`" not in sec:
                err(f"DOSSIER.template.md: {r['id']} (dossier:{key}) not listed in the {key} section")


def check_capabilities(rules: list[dict], rules_text: str) -> None:
    text = CAPABILITIES.read_text()
    caps = parse_rules(text, "capabilities.md")
    ids = [c.get("id") for c in caps]
    for i in {i for i in ids if ids.count(i) > 1}:
        err(f"capabilities.md: duplicate id {i}")
    by_id = {c["id"]: c for c in caps if "id" in c}
    manual_section = text.split("## Manual provider", 1)[-1]
    prompts = set(re.findall(r"^#### ([a-z_]+)\s*$", manual_section, re.M))
    required = {c for r in rules for c in (r.get("requires") or [])}
    for c in caps:
        cid = c.get("id", "<no id>")
        for k in ("meaning", "semantics", "freshness", "providers"):
            if k not in c:
                err(f"capabilities.md: {cid}: missing {k}:")
        prov = c.get("providers") or {}
        if not isinstance(prov, dict):
            err(f"capabilities.md: {cid}: providers: must be a mapping")
            continue
        for name in set(prov) - PROVIDERS:
            err(f"capabilities.md: {cid}: unknown provider {name!r} (known: {sorted(PROVIDERS)})")
        tools = prov.get("intervals-icu")
        if tools is not None and (not isinstance(tools, list) or not all(str(t).startswith("icu_") for t in tools)):
            err(f"capabilities.md: {cid}: intervals-icu must list icu_* tool names")
        if prov.get("manual") is True and cid not in prompts:
            err(f"capabilities.md: {cid}: manual provider without a '#### {cid}' prompt")
        if cid not in required and not c.get("display_only"):
            err(f"capabilities.md: {cid}: required by no rule and not display_only")
    for pr in sorted(prompts - {c["id"] for c in caps if (c.get("providers") or {}).get("manual") is True}):
        err(f"capabilities.md: prompt '#### {pr}' for a capability manual does not supply")
    for r in rules:
        req = r.get("requires")
        if req is None:
            continue
        if not isinstance(req, list) or not req:
            err(f"{r.get('id')}: requires: must be a non-empty list")
            continue
        for c in req:
            if c not in by_id:
                err(f"{r.get('id')}: requires unknown capability {c!r}")
            elif not by_id[c].get("providers"):
                print(f"warning: {r.get('id')} requires {c}, which no provider supplies")
    for m in re.finditer(r"\bicu_[a-z_]+", rules_text):
        err(f"RULES.md names MCP tool {m.group(0)!r}; reference a capability instead")


def version_of(text: str) -> tuple[int, ...] | None:
    m = re.match(r"# RULES v(\d+(?:\.\d+)*)", text)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None


def check_version(text: str, rules: list[dict], base: str | None) -> None:
    if version_of(text) is None:
        err("RULES.md: first line is not '# RULES v<version>'")
        return
    if not base:
        return
    try:
        old = subprocess.run(
            ["git", "show", f"{base}:RULES.md"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout
    except subprocess.CalledProcessError:
        print(f"warning: cannot read RULES.md at {base}; version check skipped")
        return
    canon = lambda rs: json.dumps(rs, sort_keys=True, default=str)  # noqa: E731
    if canon(parse_rules(old, f"{base}:RULES.md")) != canon(rules):
        new_v, old_v = version_of(text), version_of(old)
        if old_v is not None and new_v <= old_v:
            err(f"RULES.md: rule content changed against {base} but version not bumped "
                f"(v{'.'.join(map(str, old_v))} -> v{'.'.join(map(str, new_v))})")


def load_allowlist() -> list[tuple[str, str]]:
    entries = []
    if ALLOWLIST.exists():
        for line in ALLOWLIST.read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3 or not parts[2]:
                err(f"{ALLOWLIST.name}: entry needs 'path | substring | reason': {line}")
                continue
            entries.append((parts[0], parts[1]))
    return entries


def check_ownership(scan_reviews: bool) -> None:
    files = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    allow = load_allowlist()
    used = set()
    for f in files:
        if f.startswith("reviews/") and not scan_reviews:
            continue
        if f in ("tools/lint_rules.py", "tools/lint_allowlist.txt"):
            continue
        p = ROOT / f
        if p.suffix not in {".md", ".txt", ".yml", ".yaml", ".json", ".py", ""} or not p.is_file():
            continue
        for n, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
            for label, pat in OWNERSHIP_PATTERNS.items():
                for m in re.finditer(pat, line):
                    hit = [(a, s) for a, s in allow if a == f and s in line]
                    if hit:
                        used.update(hit)
                        continue
                    err(f"{f}:{n}: possible platform-owned value ({label}): {m.group(0)!r}")
    for a, s in allow:
        if (a, s) not in used:
            print(f"warning: allowlist entry unused: {a} | {s}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--base", help="git ref to compare RULES.md against for the version check")
    ap.add_argument("--scan-reviews", action="store_true", help="include reviews/ in the ownership scan")
    args = ap.parse_args()

    rules_text = RULES.read_text()
    template_text = TEMPLATE.read_text()
    rules = parse_rules(rules_text, "RULES.md")
    disciplines, fields = parse_template(template_text)
    check_rules(rules, disciplines, fields)
    check_template_lists(rules, disciplines, fields, template_text)
    check_capabilities(rules, rules_text)
    check_version(rules_text, rules, args.base)
    check_ownership(args.scan_reviews)

    for e in errors:
        print(f"error: {e}")
    print(f"{len(rules)} rules, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
