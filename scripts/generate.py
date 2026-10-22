#!/usr/bin/env python3
"""Генерирует REGISTER.md и register.json. --check: упасть, если файлы устарели."""
import json, sys, collections
from reqlib import ROOT, files, parse
rows = []
for p in files():
    fm, _ = parse(p); fm["path"] = str(p.relative_to(ROOT)); rows.append(fm)
rows.sort(key=lambda r: r["id"])
js = json.dumps(rows, ensure_ascii=False, indent=2, default=str) + "\n"
cnt = collections.Counter((r["scope"], r["type"]) for r in rows)
st = collections.Counter(r["status"] for r in rows)
md = ["# Реестр требований", "", "*Сгенерирован `scripts/generate.py` — не редактировать вручную.*", "",
      f"Всего: **{len(rows)}**. По статусам: " + ", ".join(f"{k} {v}" for k, v in sorted(st.items())), "",
      "| Область | Тип | Кол-во |", "|---|---|---|"]
md += [f"| {a} | {b} | {n} |" for (a, b), n in sorted(cnt.items())]
md += ["", "| ID | Название | Тип | Статус | Приоритет | Владелец | Область | ADR |", "|---|---|---|---|---|---|---|---|"]
for r in rows:
    adr = ", ".join((r.get("links") or {}).get("adr", []))
    md.append(f"| [{r['id']}]({r['path']}) | {r['title']} | {r['type']} | {r['status']} | {r['priority']} | {r['owner']} | {r['scope']} | {adr} |")
md = "\n".join(md) + "\n"
out = {ROOT / "REGISTER.md": md, ROOT / "register.json": js}
if "--check" in sys.argv:
    stale = [p.name for p, c in out.items() if not p.exists() or p.read_text(encoding="utf-8") != c]
    if stale: print("Устарели:", stale, "— запустите scripts/generate.py"); sys.exit(1)
    print("REGISTER.md и register.json актуальны"); sys.exit(0)
for p, c in out.items(): p.write_text(c, encoding="utf-8")
print(f"Сгенерировано: {len(rows)} записей")
