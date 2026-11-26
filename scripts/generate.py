#!/usr/bin/env python3
"""Генерирует REGISTER.md, CATALOG.md, register.json, catalog/ids.lock и копии принятых
типовых требований requirements/_catalog/*.md по adoption.yaml.
--check: упасть, если хоть один файл устарел (CI)."""
import collections, json, re, sys
from reqlib import (ROOT, CFG, roots, files, parse, section, load_yaml, profiles, catalog_items,
                    expand_profile, render_params, generated_files, GENERATED_DIR, FM)
import yaml

out = {}
project_rows, catalog_rows = [], []
for p in files():
    fm, _ = parse(p)
    fm["path"] = str(p.relative_to(ROOT))
    kind = roots()[p.relative_to(ROOT).parts[0]].get("kind", "project")
    (catalog_rows if kind == "typical" else project_rows).append(fm)
project_rows.sort(key=lambda r: r["id"])
catalog_rows.sort(key=lambda r: r["id"])
PROFS = profiles()
CAT = catalog_items()

# --- копии принятых типовых требований -----------------------------------------------------
gen_dir_root = None
ad_path = ROOT / "adoption.yaml"
generated = {}
if ad_path.exists():
    ad = load_yaml(ad_path)
    proj_root = ad.get("root", "requirements")
    gen_dir_root = ROOT / proj_root / GENERATED_DIR
    wanted = {}
    for pid in ad.get("profiles", []):
        if pid in PROFS: wanted.update(expand_profile(pid, PROFS))
    release = (ad.get("catalog") or {}).get("release", "")
    for it in ad.get("items", []) or []:
        t, mode = it["id"], it["mode"]
        if mode == "waive" or t not in CAT: continue
        p, fm, body = CAT[t]
        prof = wanted.get(t, {})
        params = {k: v["default"] for k, v in (fm.get("params") or {}).items()}
        params.update(prof.get("params") or {})
        params.update(it.get("params") or {})
        needs = "Needs: impl, itest" if mode == "inherit" else "Needs: req"
        body2 = re.sub(r"^Needs:.*$", needs, render_params(body, params), count=1, flags=re.M)
        body2 = re.sub(r"\n## Параметры\n.*?(?=^## |\Z)", "\n", body2, flags=re.S | re.M)
        adoption = {"mode": mode, "catalog_release": release}
        if it.get("priority"): adoption["priority"] = it["priority"]
        if params: adoption["params"] = params
        if it.get("by"): adoption["by"] = it["by"]
        head = {k: fm[k] for k in ("id", "title", "type", "status", "owner", "scope", "capability") if k in fm}
        head["level"] = prof.get("level") or fm.get("level")
        head["source"] = [f"catalog-v{release}: {p.relative_to(ROOT)}"]
        head["version"] = fm.get("version", 1)
        head["adoption"] = adoption
        text = ("---\n" + yaml.safe_dump(head, allow_unicode=True, sort_keys=False, width=1000) + "---\n"
                "<!-- Сгенерировано scripts/generate.py из каталога по adoption.yaml. Не редактировать. -->\n" + body2.rstrip() + "\n")
        generated[gen_dir_root / f"{t}.md"] = text
out.update(generated)

# --- REGISTER.md (проект) ------------------------------------------------------------------
gen_rows = []
for path, text in sorted(generated.items()):
    fm = yaml.safe_load(FM.match(text).group(1)); fm["path"] = str(path.relative_to(ROOT)); gen_rows.append(fm)
cnt = collections.Counter((r["scope"], r["type"]) for r in project_rows)
stc = collections.Counter(r["status"] for r in project_rows)
md = ["# Реестр требований", "", "*Сгенерирован `scripts/generate.py`, не редактировать вручную.*", "",
      f"Всего требований проекта: **{len(project_rows)}**. По статусам: " + ", ".join(f"{k} {v}" for k, v in sorted(stc.items())),
      "", "Приоритет по MoSCoW: M Must, S Should, C Could, W Won't.", "",
      "| Область | Тип | Кол-во |", "|---|---|---|"]
md += [f"| {a} | {b} | {n} |" for (a, b), n in sorted(cnt.items())]
md += ["", "| ID | Название | Тип | Статус | Приоритет | Владелец | Область | Уточняет | ADR |", "|---|---|---|---|---|---|---|---|---|"]
for r in project_rows:
    adr = ", ".join((r.get("links") or {}).get("adr", []))
    md.append(f"| [{r['id']}]({r['path']}) | {r['title']} | {r['type']} | {r['status']} | {r.get('priority', '')} | {r['owner']} | {r['scope']} | {', '.join(r.get('refines', []))} | {adr} |")
if ad_path.exists():
    ad = load_yaml(ad_path)
    md += ["", "## Принятые типовые требования", "",
           f"Каталог: выпуск {ad['catalog']['release']}, профили: {', '.join(ad['profiles'])}. Подробности в `adoption.yaml`.", "",
           "| ID | Название | Режим | Приоритет | Уровень | Чем уточнено, причина исключения |", "|---|---|---|---|---|---|"]
    for it in ad.get("items", []):
        t = it["id"]; c = CAT.get(t, (None, {}, ""))[1]
        link = f"[{t}](requirements/{GENERATED_DIR}/{t}.md)" if it["mode"] != "waive" else t
        extra = ", ".join(it.get("by", [])) if it["mode"] == "refine" else (f"{it.get('reason', '')} (до {it.get('review', '')}, {it.get('owner', '')})" if it["mode"] == "waive" else "")
        md.append(f"| {link} | {c.get('title', '')} | {it['mode']} | {it.get('priority', '')} | {c.get('level', '')} | {extra} |")
out[ROOT / "REGISTER.md"] = "\n".join(md) + "\n"

# --- CATALOG.md ----------------------------------------------------------------------------
member = collections.defaultdict(list)
for pid, (_, data) in PROFS.items():
    for it in data.get("items", []) or []:
        member[it["id"]].append(f"{pid} ({it.get('level') or CAT.get(it['id'], (0, {}, 0))[1].get('level', '')})")
by_dom = collections.defaultdict(list)
for r in catalog_rows: by_dom[r["scope"]].append(r)
cm = ["# Каталог типовых требований", "", "*Сгенерирован `scripts/generate.py`, не редактировать вручную.*", "",
      f"Выпуск каталога: **{CFG.get('catalog_release')}**. Типовых требований: **{len(catalog_rows)}**. Профилей: **{len(PROFS)}**.",
      "", "Уровень (MUST, SHOULD, MAY) — сила формулировки по RFC 2119 и RFC 8174. Приоритет по MoSCoW задаёт проект в `adoption.yaml`.", "",
      "## Профили", "", "| Профиль | Вид | Версия | Статус | Blueprint | Включает | Пунктов (с включёнными) |", "|---|---|---|---|---|---|---|"]
for pid, (p, data) in sorted(PROFS.items()):
    cm.append(f"| [{pid}]({p.relative_to(ROOT)}) | {data.get('kind')} | {data.get('version')} | {data.get('status')} | {data.get('blueprint', '')} | {', '.join(data.get('includes', []) or [])} | {len(data.get('items') or [])} ({len(expand_profile(pid, PROFS))}) |")
cm += ["", "## Требования по доменам naming-standard", ""]
for dom in sorted(by_dom):
    cm += [f"### {dom}", "", "| ID | Название | Возможность | Уровень | Статус | Профили | Проверки blueprints |", "|---|---|---|---|---|---|---|"]
    for r in by_dom[dom]:
        cm.append(f"| [{r['id']}]({r['path']}) | {r['title']} | {r.get('capability', '')} | {r.get('level', '')} | {r['status']} | {', '.join(member.get(r['id'], []))} | {', '.join(r.get('checks', []))} |")
    cm.append("")
srcs = load_yaml(ROOT / "sources.yaml").get("sources", {}) if (ROOT / "sources.yaml").exists() else {}
used_by = collections.defaultdict(list)
for r in catalog_rows:
    for k in r.get("basis", []): used_by[k].append(r["id"])
cm += ["## Источники и где они используются", "", "| Ключ | Источник | Используется в |", "|---|---|---|"]
for k, s in sorted(srcs.items()):
    cm.append(f"| `{k}` | [{s.get('title')}]({s.get('url')}) | {', '.join(used_by.get(k, [])) or '—'} |")
out[ROOT / "CATALOG.md"] = "\n".join(cm) + "\n"

# --- register.json и журнал ID -------------------------------------------------------------
allrows = project_rows + catalog_rows + gen_rows
out[ROOT / "register.json"] = json.dumps(allrows, ensure_ascii=False, indent=2, default=str) + "\n"
lock = ROOT / "catalog" / "ids.lock"
issued = set()
if lock.exists():
    issued = {l.strip() for l in lock.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
issued |= {r["id"] for r in catalog_rows}
out[lock] = ("# Журнал выданных ID каталога. Дописывает scripts/generate.py. Номер из журнала не переиспользуется.\n"
             + "\n".join(sorted(issued)) + "\n")

stale_generated = [p for p in generated_files() if p not in generated]
if "--check" in sys.argv:
    stale = [str(p.relative_to(ROOT)) for p, c in out.items() if not p.exists() or p.read_text(encoding="utf-8") != c]
    stale += [str(p.relative_to(ROOT)) + " (лишний)" for p in stale_generated]
    if stale:
        print("Устарели:", stale, "; запустите scripts/generate.py"); sys.exit(1)
    print(f"Сгенерированные файлы актуальны: {len(out)}"); sys.exit(0)
for p in stale_generated: p.unlink()
for p, c in out.items():
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(c, encoding="utf-8")
print(f"Сгенерировано: {len(out)} файлов; требований проекта {len(project_rows)}, типовых {len(catalog_rows)}, копий принятых {len(generated)}")
