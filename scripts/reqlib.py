"""Общие функции: конфиг, обход файлов, разбор Markdown + YAML front matter."""
import pathlib, re, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = yaml.safe_load((ROOT / "reqs.config.yaml").read_text(encoding="utf-8"))
FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)

def files():
    for base in CFG["roots"]:
        d = ROOT / base
        if d.exists():
            yield from sorted(p for p in d.rglob("*.md") if p.name != "README.md")

def parse(p):
    m = FM.match(p.read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"{p.relative_to(ROOT)}: нет YAML front matter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)
