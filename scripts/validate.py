#!/usr/bin/env python3
"""Валидатор: схема, конфиг (префиксы/типы/области), имя файла = id, уникальность,
depends_on, ADR существует, раздел приёмки, OFT-маркер, у verified есть доказательства.
Флаги: --mode warn|error (перекрывает конфиг), --report FILE (отчёт нарушений в Markdown)."""
import argparse, json, re, sys
from jsonschema import Draft202012Validator
from reqlib import ROOT, CFG, files, parse

ap = argparse.ArgumentParser(); ap.add_argument("--mode", choices=["warn", "error"]); ap.add_argument("--report")
a = ap.parse_args()
st = CFG.get("strictness", {})
def level(rule): return a.mode or st.get("rules", {}).get(rule, st.get("default", "error"))

V = Draft202012Validator(json.loads((ROOT / "schema/requirement.schema.json").read_text()))
issues, items = [], {}
def add(rule, rel, msg): issues.append((level(rule), rule, str(rel), msg))

adr_dir = ROOT / CFG.get("adr_dir", "docs/adr")
adrs = {p.name.split("-")[0] + "-" + p.name.split("-")[1] for p in adr_dir.glob("ADR-*.md")} if adr_dir.exists() else set()

for p in files():
    rel = p.relative_to(ROOT)
    try: fm, body = parse(p)
    except Exception as e: add("schema", rel, str(e)); continue
    for e in V.iter_errors(fm): add("schema", rel, f"{'/'.join(map(str, e.path)) or '-'}: {e.message}")
    i = str(fm.get("id", ""))
    pre = CFG["roots"][rel.parts[0]]
    for field, allowed in (("type", CFG["types"]), ("scope", CFG["scopes"]), ("status", CFG["statuses"]), ("priority", CFG["priorities"])):
        if fm.get(field) not in allowed: add("config", rel, f"{field}={fm.get(field)!r} не из {allowed}")
    if p.stem != i: add("filename", rel, f"имя файла должно быть {i}.md")
    if i in items: add("duplicate", rel, f"дубликат id {i}")
    items[i] = fm
    if not i.startswith(pre + "-"): add("prefix", rel, f"префикс должен быть {pre}")
    if i.split("-")[1:2] != [fm.get("type")]: add("type", rel, "type не совпадает с id")
    if len(rel.parts) < 3 or rel.parts[1] != fm.get("scope"): add("scope_dir", rel, f"каталог ≠ scope {fm.get('scope')}")
    if CFG["acceptance_heading"] not in body: add("acceptance_section", rel, f"нет раздела «{CFG['acceptance_heading']}»")
    if CFG.get("require_oft_marker") and f"req~{i}~" not in body: add("oft_marker", rel, f"нет OFT-маркера `req~{i}~N`")
    links = fm.get("links") or {}
    for x in links.get("adr", []):
        if x not in adrs: add("adr_exists", rel, f"ADR {x} не найден в {CFG.get('adr_dir')}")
    if fm.get("status") == "verified" and not links.get("verified_by"):
        add("verified_needs_evidence", rel, "status=verified без links.verified_by")
for i, fm in items.items():
    for d in (fm.get("links") or {}).get("depends_on", []):
        if d not in items: add("depends_on", i, f"depends_on {d} не найден")

errs = [x for x in issues if x[0] == "error"]
for lv, rule, rel, msg in issues: print(f"{lv.upper():5} [{rule}] {rel}: {msg}")
print(f"{len(items)} требований, ошибок: {len(errs)}, предупреждений: {len(issues) - len(errs)}")
if a.report:
    lines = ["# Отчёт валидатора", "", "| Уровень | Правило | Файл | Сообщение |", "|---|---|---|---|"]
    lines += [f"| {lv} | {r} | {f} | {m.replace('|', '/')} |" for lv, r, f, m in issues]
    open(a.report, "w", encoding="utf-8").write("\n".join(lines) + "\n")
sys.exit(1 if errs else 0)
