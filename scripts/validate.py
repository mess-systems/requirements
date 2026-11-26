#!/usr/bin/env python3
"""Валидатор требований проекта и каталога типовых требований.

Проверяет: схему front matter, словари reqs.config.yaml по корню, имя файла = id, уникальность,
префикс и тип в id, каталог = scope, раздел приёмки, маркер OpenFastTrace, depends_on, ADR,
доказательства у verified. Для каталога ещё: коды доменов и возможностей naming-standard,
уровень, контуры, ревизию, параметры, ключи sources.yaml, строки матриц blueprints, карточки
tech-radar, нейтральность формулировок, подсказки ISO/IEC/IEEE 29148, журнал выданных ID.
Профили (profiles/), adoption.yaml и приватность всех текстов.

Флаги: --mode warn|error (перекрывает конфиг), --report FILE (отчёт в Markdown).
Переменные окружения: NAMING=путь к клону naming-standard, BLUEPRINTS=путь к клону blueprints.
"""
import argparse, datetime, json, os, pathlib, re, sys
from jsonschema import Draft202012Validator
from reqlib import (ROOT, CFG, roots, files, parse, section, load_yaml, profiles,
                    expand_profile, GENERATED_DIR)

ap = argparse.ArgumentParser()
ap.add_argument("--mode", choices=["warn", "error"])
ap.add_argument("--report")
a = ap.parse_args()
st = CFG.get("strictness", {})


def level(rule):
    return a.mode or st.get("rules", {}).get(rule, st.get("default", "error"))


issues = []


def add(rule, rel, msg):
    issues.append((level(rule), rule, str(rel), msg))


def schema(name):
    return Draft202012Validator(json.loads((ROOT / "schema" / name).read_text(encoding="utf-8")))


V_REQ, V_PROF, V_ADOPT = schema("requirement.schema.json"), schema("profile.schema.json"), schema("adoption.schema.json")

# --- словари -------------------------------------------------------------------------------
NS = CFG.get("naming_standard", {})
CAPS = {d: set(c) for d, c in NS.get("capabilities", {}).items()}
PENDING = {d: set(c) for d, c in (NS.get("pending") or {}).items()}
naming_dir = os.environ.get("NAMING")
if naming_dir and (pathlib.Path(naming_dir) / "01-naming-conventions.md").exists():
    doc = (pathlib.Path(naming_dir) / "01-naming-conventions.md").read_text(encoding="utf-8")
    part = doc.split("### 4.3 Capability codes", 1)[1].split("\n### ", 1)[0]
    live = {}
    for m in re.finditer(r"^\| `([a-z]+)` \| `([^`]+)` \|", part, re.M):
        live[m.group(1)] = set(m.group(2).split())
    for d in set(live) | set(CAPS):
        if live.get(d, set()) != CAPS.get(d, set()):
            add("naming_snapshot", "reqs.config.yaml",
                f"снимок кодов домена {d} расходится со стандартом в {naming_dir}: {sorted(CAPS.get(d, set()))} против {sorted(live.get(d, set()))}")
    CAPS = live

SOURCES = load_yaml(ROOT / "sources.yaml").get("sources", {}) if (ROOT / "sources.yaml").exists() else {}

RADAR = {}
rp = ROOT / "schema" / "radar-names.txt"
if rp.exists():
    for line in rp.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            slug, _, title = line.partition("|")
            RADAR[slug] = re.sub(r"\s*\(.*\)$", "", title or slug)
ALLOW = set((CFG.get("neutrality") or {}).get("allow", []))

BP_ROWS = None
bp_dir = os.environ.get("BLUEPRINTS")
if bp_dir and pathlib.Path(bp_dir).is_dir():
    BP_ROWS = set()
    for readme in pathlib.Path(bp_dir).glob("*/README.ru.md"):
        for m in re.finditer(r"^\| ([A-Z]+[0-9]+) \|", readme.read_text(encoding="utf-8"), re.M):
            BP_ROWS.add(f"{readme.parent.name}#{m.group(1)}")

adr_dir = ROOT / CFG.get("adr_dir", "docs/adr")
adrs = {"-".join(p.name.split("-")[:2]) for p in adr_dir.glob("ADR-*.md")} if adr_dir.exists() else set()
VAGUE = (CFG.get("quality") or {}).get("vague_words", [])
PLACEHOLDER = re.compile(r"\{([a-z][a-z0-9_]*)\}")

# --- требования ----------------------------------------------------------------------------
items, kinds = {}, {}
for p in files():
    rel = p.relative_to(ROOT)
    rc = roots()[rel.parts[0]]
    kind = rc.get("kind", "project")
    try:
        fm, body = parse(p)
    except Exception as e:
        add("schema", rel, str(e)); continue
    for e in V_REQ.iter_errors(fm):
        add("schema", rel, f"{'/'.join(map(str, e.path)) or '-'}: {e.message}")
    i = str(fm.get("id", ""))
    for field, allowed in (("type", rc["types"]), ("scope", rc["scopes"]), ("status", rc["statuses"])):
        if fm.get(field) not in allowed:
            add("config", rel, f"{field}={fm.get(field)!r} не из {allowed}")
    if p.stem != i: add("filename", rel, f"имя файла должно быть {i}.md")
    if i in items: add("duplicate", rel, f"дубликат id {i}")
    items[i], kinds[i] = fm, kind
    if not i.startswith(rc["prefix"] + "-"): add("prefix", rel, f"префикс должен быть {rc['prefix']}")
    if i.split("-")[1:2] != [fm.get("type")]: add("type", rel, "type не совпадает с id")
    if len(rel.parts) < 3 or rel.parts[1] != fm.get("scope"): add("scope_dir", rel, f"каталог ≠ scope {fm.get('scope')}")
    if CFG["acceptance_heading"] not in body: add("acceptance_section", rel, f"нет раздела «{CFG['acceptance_heading']}»")
    ver = fm.get("version", 1)
    if CFG.get("require_oft_marker") and f"req~{i}~" not in body:
        add("oft_marker", rel, f"нет маркера OpenFastTrace `req~{i}~N`")
    elif f"req~{i}~{ver}`" not in body and f"req~{i}~{ver}\n" not in body:
        add("oft_marker", rel, f"ревизия маркера OpenFastTrace не совпадает с version={ver}")
    links = fm.get("links") or {}
    for x in links.get("adr", []):
        if x not in adrs: add("adr_exists", rel, f"ADR {x} не найден в {CFG.get('adr_dir')}")
    if fm.get("status") == "verified" and not links.get("verified_by"):
        add("verified_needs_evidence", rel, "status=verified без links.verified_by")

    if kind == "project":
        if fm.get("priority") not in rc.get("priorities", []):
            add("config", rel, f"priority={fm.get('priority')!r} не из {rc.get('priorities')} (MoSCoW)")
        for f in ("level", "capability", "params", "applies_to"):
            if f in fm: add("config", rel, f"поле {f} задаётся только в каталоге")
        continue

    # каталог типовых требований
    for f in ("capability", "level", "applies_to", "version"):
        if f not in fm: add("schema", rel, f"в типовом требовании обязательно поле {f}")
    if "priority" in fm: add("config", rel, "приоритет задаёт проект (MoSCoW), в каталоге его нет")
    dom = fm.get("scope")
    if fm.get("type", "").lower() != dom: add("type", rel, "type должен быть кодом домена scope в верхнем регистре")
    cap = fm.get("capability")
    if cap not in CAPS.get(dom, set()) | PENDING.get(dom, set()):
        add("capability", rel, f"код возможности {cap!r} не найден в домене {dom} naming-standard")
    elif cap in PENDING.get(dom, set()):
        add("capability_pending", rel, f"код {dom}/{cap} предложен, но ещё не внесён в naming-standard")
    if fm.get("level") not in CFG["levels"]: add("config", rel, f"level={fm.get('level')!r} не из {CFG['levels']}")
    for c in fm.get("applies_to", []):
        if c not in CFG["contours"]: add("config", rel, f"контур {c!r} не из {CFG['contours']}")
    params = fm.get("params") or {}
    used = set(PLACEHOLDER.findall(body))
    for x in used - set(params): add("params_declared", rel, f"параметр {{{x}}} есть в тексте, но не объявлен")
    for x in set(params) - used: add("params_declared", rel, f"параметр {x} объявлен, но не используется в тексте")
    for k in fm.get("basis", []):
        if k not in SOURCES: add("basis", rel, f"ключ {k!r} не найден в sources.yaml")
    for c in fm.get("checks", []):
        if BP_ROWS is None: continue
        if c not in BP_ROWS: add("blueprint_check", rel, f"строка матрицы {c} не найдена в {bp_dir}")
    for r in fm.get("realizations", []):
        if RADAR and r not in RADAR: add("realizations", rel, f"карточки {r!r} нет в schema/radar-names.txt")
    normative = section(body, "Требование") + "\n" + section(body, "Критерии приёмки")
    for slug, title in RADAR.items():
        if slug in ALLOW: continue
        for name in {slug, title}:
            if re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", normative, re.I):
                add("neutrality", rel, f"название продукта «{name}» в нормативном тексте; перенесите в realizations"); break
    stmt = "\n".join(l for l in section(body, "Требование").splitlines()
                     if l.strip() and not l.startswith(("`req~", "Needs:", "Tags:", "Covers:")))
    if len(re.findall(r"\bдолжн", stmt, re.I)) > 1:
        add("quality_singular", rel, "в формулировке больше одного «должна»: требование не единичное (29148, 5.2.5)")
    for w in VAGUE:
        if w.lower() in normative.lower():
            add("quality_vague", rel, f"размытое слово «{w}»: требование трудно проверить (29148, 5.2.5)")

# depends_on и refines
for i, fm in items.items():
    for d in (fm.get("links") or {}).get("depends_on", []):
        if d not in items: add("depends_on", i, f"depends_on {d} не найден")
    for t in fm.get("refines", []):
        if kinds.get(t) != "typical": add("refines", i, f"refines {t}: такого типового требования нет")

# журнал выданных ID каталога: номер не переиспользуется, файл не удаляется
lock = ROOT / "catalog" / "ids.lock"
if lock.exists():
    issued = {l.strip() for l in lock.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
    for x in sorted(issued - {i for i, k in kinds.items() if k == "typical"}):
        add("id_reuse", "catalog/ids.lock", f"{x} выдан ранее, но файла нет: требования не удаляют, а переводят в deprecated")

# --- профили -------------------------------------------------------------------------------
PROFS = profiles()
for pid, (p, data) in PROFS.items():
    rel = p.relative_to(ROOT)
    for e in V_PROF.iter_errors(data):
        add("profile", rel, f"{'/'.join(map(str, e.path)) or '-'}: {e.message}")
    if p.stem != pid: add("profile", rel, f"имя файла должно быть {pid}.yaml")
    expected = {"sets": "set", "classes": "class"}.get(p.parent.name)
    if data.get("kind") != expected: add("profile", rel, f"kind должен быть {expected}")
    if data.get("kind") == "class" and data.get("blueprint") and data["blueprint"] != pid:
        add("profile", rel, "имя профиля класса должно совпадать с папкой blueprint")
    seen = set()
    for it in data.get("items", []) or []:
        t = it.get("id")
        if t in seen: add("profile", rel, f"{t} указан дважды")
        seen.add(t)
        if kinds.get(t) != "typical": add("profile", rel, f"{t} нет в каталоге"); continue
        if items[t].get("status") == "deprecated": add("profile", rel, f"{t} в статусе deprecated")
        for k in (it.get("params") or {}):
            if k not in (items[t].get("params") or {}): add("profile", rel, f"{t}: параметр {k} не объявлен в требовании")
    for inc in data.get("includes", []) or []:
        name, _, ver = inc.partition("@")
        if name not in PROFS: add("profile", rel, f"includes {inc}: профиля нет"); continue
        if not PROFS[name][1].get("version", "").startswith(ver + "."):
            add("profile", rel, f"includes {inc}: версия профиля {name} = {PROFS[name][1].get('version')}")
    try: expand_profile(pid, PROFS)
    except ValueError as e: add("profile", rel, str(e))

# --- adoption.yaml -------------------------------------------------------------------------
ad_path = ROOT / "adoption.yaml"
if ad_path.exists():
    ad = json.loads(json.dumps(load_yaml(ad_path), default=str))  # даты YAML как строки
    for e in V_ADOPT.iter_errors(ad):
        add("adoption", "adoption.yaml", f"{'/'.join(map(str, e.path)) or '-'}: {e.message}")
    if (ad.get("catalog") or {}).get("release") != CFG.get("catalog_release"):
        add("adoption_release", "adoption.yaml", f"release {ad.get('catalog', {}).get('release')} ≠ catalog_release {CFG.get('catalog_release')}")
    wanted = {}
    for pid in ad.get("profiles", []):
        if pid not in PROFS: add("adoption", "adoption.yaml", f"профиля {pid} нет"); continue
        wanted.update(expand_profile(pid, PROFS))
    chosen = {}
    today = datetime.date.today().isoformat()
    for it in ad.get("items", []) or []:
        t = it.get("id")
        if t in chosen: add("adoption", "adoption.yaml", f"{t} указан дважды")
        chosen[t] = it
        if kinds.get(t) != "typical": add("adoption", "adoption.yaml", f"{t} нет в каталоге"); continue
        for k in (it.get("params") or {}):
            if k not in (items[t].get("params") or {}): add("adoption", "adoption.yaml", f"{t}: параметр {k} не объявлен")
        if it.get("mode") == "refine":
            for b in it.get("by", []):
                if kinds.get(b) != "project": add("adoption", "adoption.yaml", f"{t}: требования проекта {b} нет"); continue
                if t not in items[b].get("refines", []): add("adoption", "adoption.yaml", f"{b} должно содержать refines: [{t}]")
        if it.get("mode") == "waive" and str(it.get("review", "9999")) < today:
            add("waiver_expired", "adoption.yaml", f"{t}: срок пересмотра исключения {it.get('review')} истёк")
    for t, w in wanted.items():
        lvl = w.get("level") or items.get(t, {}).get("level")
        if lvl == "MUST" and t not in chosen:
            add("adoption_coverage", "adoption.yaml", f"{t} (MUST в профиле {w['from']}) не принят, не уточнён и не исключён")

# --- приватность ---------------------------------------------------------------------------
PRIV = [
    ("IPv4-адрес", re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")),
    ("имя хоста во внутренней зоне", re.compile(r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:lan|local|internal|intranet|localdomain|home\.arpa)\b", re.I)),
    ("символ параграфа", re.compile("\u00a7")),
    ("адрес почты", re.compile(r"\b[\w.+-]+@(?!mess\.systems\b|example\.(?:com|org)\b)[A-Za-z][\w-]*(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")),
]
priv_targets = [ROOT / d for d in ("catalog", "profiles", "assessments", "requirements", "docs", "templates")] + \
               [ROOT / f for f in ("adoption.yaml", "sources.yaml", "CATALOG.md", "README.md", "README.ru.md", "README.zh-CN.md")]
for t in priv_targets:
    for p in ([t] if t.is_file() else sorted(t.rglob("*")) if t.is_dir() else []):
        if p.suffix not in (".md", ".yaml", ".yml", ".lock") or not p.is_file(): continue
        text = p.read_text(encoding="utf-8")
        for name, rx in PRIV:
            m = rx.search(text)
            if m: add("privacy", p.relative_to(ROOT), f"{name}: «{m.group(0)}»")

# --- итог ----------------------------------------------------------------------------------
errs = [x for x in issues if x[0] == "error"]
for lv, rule, rel, msg in issues: print(f"{lv.upper():5} [{rule}] {rel}: {msg}")
n_typ = sum(1 for k in kinds.values() if k == "typical")
print(f"{len(items) - n_typ} требований проекта, {n_typ} типовых, {len(PROFS)} профилей; ошибок: {len(errs)}, предупреждений: {len(issues) - len(errs)}")
if BP_ROWS is None: print("строки матриц blueprints не сверялись (задайте BLUEPRINTS=путь к клону)")
if a.report:
    lines = ["# Отчёт валидатора", "", "| Уровень | Правило | Файл | Сообщение |", "|---|---|---|---|"]
    lines += [f"| {lv} | {r} | {f} | {m.replace('|', '/')} |" for lv, r, f, m in issues]
    open(a.report, "w", encoding="utf-8").write("\n".join(lines) + "\n")
sys.exit(1 if errs else 0)
