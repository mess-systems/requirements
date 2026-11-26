"""Общие функции: конфиг, корни, обход файлов, разбор Markdown + YAML front matter, профили."""
import pathlib, re, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "reqs.config.yaml").read_text(encoding="utf-8"))
FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
GENERATED_DIR = "_catalog"   # requirements/_catalog: копии типовых требований, принятых проектом


def roots():
    return CFG["roots"]


def files(root=None):
    """Все файлы требований (без README и без сгенерированных копий _catalog)."""
    for base in roots():
        if root and base != root:
            continue
        d = ROOT / base
        if d.exists():
            yield from sorted(p for p in d.rglob("*.md")
                              if p.name != "README.md" and GENERATED_DIR not in p.relative_to(ROOT).parts)


def generated_files():
    for base, rc in roots().items():
        d = ROOT / base / GENERATED_DIR
        if rc.get("kind") == "project" and d.exists():
            yield from sorted(d.glob("*.md"))


def parse(p):
    m = FM.match(p.read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"{p.relative_to(ROOT)}: нет YAML front matter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def section(body, heading):
    """Текст раздела «## heading» до следующего заголовка второго уровня."""
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def load_yaml(p):
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def profiles():
    """{id: (path, data)} для profiles/sets и profiles/classes."""
    out = {}
    for p in sorted((ROOT / "profiles").glob("*/*.yaml")):
        data = load_yaml(p)
        out[data.get("id", p.stem)] = (p, data)
    return out


def catalog_items():
    items = {}
    for p in files("catalog"):
        fm, body = parse(p)
        items[str(fm.get("id"))] = (p, fm, body)
    return items


def expand_profile(pid, profs, seen=None):
    """Плоский список пунктов профиля с учётом includes: {id: {level, params, stage, from}}."""
    seen = seen or set()
    if pid in seen:
        raise ValueError(f"цикл includes в профиле {pid}")
    seen.add(pid)
    _, data = profs[pid]
    out = {}
    for inc in data.get("includes", []) or []:
        name = inc.split("@")[0]
        if name in profs:
            out.update(expand_profile(name, profs, set(seen)))
    excluded = {e["id"] for e in data.get("excluded", []) or []}
    for it in data.get("items", []) or []:
        out[it["id"]] = dict(it, **{"from": pid})
    for x in excluded:
        out.pop(x, None)
    return out


def render_params(text, params):
    return re.sub(r"\{([a-z][a-z0-9_]*)\}", lambda m: str(params.get(m.group(1), m.group(0))), text)
