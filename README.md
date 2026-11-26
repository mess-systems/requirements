**English** | [Русский](README.ru.md) | [简体中文](README.zh-CN.md)

# mess.systems requirements: requirements as code

A template for keeping requirements as code: Markdown with YAML front matter in git, checks in CI, a generated register, ADRs, tracing to code with [OpenFastTrace](https://github.com/itsallcode/openfasttrace) (OFT), a site built with MkDocs, and ready rules and prompts for AI agents. The examples describe **x**, the fictional product of the fictional company mess.systems.

The working language of the examples, prompts and process documents is Russian. This README and the zh-CN one describe the package; the content itself is not translated yet.

## Why
- Requirements are versioned and reviewed like code, through a pull request approved by a human.
- Every requirement is testable (acceptance criteria) and traceable to code and tests.
- Agents follow the same rules as people and never raise a status on their own.

## Quick start
```bash
# 1. Create a repository from this template, then
python3 -m pip install -r requirements-dev.txt
# 2. Set the prefix, types and scopes of your product
$EDITOR reqs.config.yaml
# 3. Check the examples, then replace them with your own
make check                      # validation and REGISTER.md freshness
# 4. Tracing and site (optional)
make trace IMPL=../my-service   # needs oft (OpenFastTrace 4.11) or Java 21 and the jar; TRACE_STRICT=1 fails on any defect
python3 -m pip install -r requirements-docs.txt && make site
```

## Typical requirements catalogue

The repository also holds a **catalogue of typical requirements** for classes of solutions, such as any AI gateway or any agentic delivery workspace. A typical requirement is written once in `catalog/<domain>/T-<DOM>-NNN.md` (domain codes come from the naming standard), names no products, keeps thresholds as parameters, and links to rows of blueprint check matrices. Profiles in `profiles/sets/` and `profiles/classes/` group them; a class profile is named after its blueprint folder. A project lists profiles in `adoption.yaml` and inherits, refines or waives each requirement; every MUST item must be covered and every waiver needs a reason, an owner and a review date. Project priorities use MoSCoW (M, S, C, W); MUST, SHOULD and MAY in the catalogue express the strength of a statement (RFC 2119, RFC 8174). The catalogue is written in Russian first; see [docs/catalog.md](docs/catalog.md) and [docs/adoption.md](docs/adoption.md).

## Principles
1. **One file, one requirement.** File name is the ID, folder is the scope.
2. **Configuration, not code.** Prefixes, types, scopes and statuses live in `reqs.config.yaml`.
3. **Testable.** A mandatory acceptance section and an OFT marker `req~ID~N`.
4. **Traceable.** `[impl->req~ID~1]` in code, `[utest->req~ID~1]` or `[itest->req~ID~1]` in tests.
5. **The register is generated.** Nobody edits it by hand; CI checks it is current.
6. **A human decides.** `approved` and `verified` are set only through an approved pull request.
7. **Strictness in stages.** Warn first, fix, then make the rule an error.
8. **Nothing sensitive.** No secrets, personal data, people's names or internal addresses.

## Contents
| Path | What |
|---|---|
| `reqs.config.yaml` | prefixes, types, scopes, strictness |
| `schema/requirement.schema.json` | JSON Schema of the front matter |
| `templates/` | requirement and ADR templates |
| `requirements/<scope>/` | 14 sample requirements of product x |
| `scripts/` | validator and register generator |
| `REGISTER.md`, `register.json` | generated register |
| `docs/adr/`, `docs/process/`, `docs/prompts/` | 2 sample ADRs, process, 8 prompts for agents |
| `docs/naming-standard.md` | how the package uses the naming standard v2.5 |
| `.cursor/rules/`, `AGENTS.md` | rules for agents |
| `.github/workflows/`, `.forgejo/workflows/` | CI for GitHub Actions and Forgejo Actions |
| `examples/` | project layouts, an implementation repository with OFT tags |

## How it fits with other mess.systems repositories

| Repository | What it gives |
|---|---|
| [naming-standard](https://github.com/mess-systems/naming-standard) | names of products, domains, environments, owners and resources used in acceptance criteria; see [docs/naming-standard.md](docs/naming-standard.md) |
| [tech-radar](https://github.com/mess-systems/tech-radar) | the tools used here: OpenFastTrace, MkDocs Material, GitHub Actions, [Forgejo](https://github.com/mess-systems/tech-radar/blob/main/technologies/forgejo.md) Actions |
| [blueprints](https://github.com/mess-systems/blueprints) | reference architectures; their requirements can be kept with this package |

## License

Text (documentation, requirements, ADRs, prompts) is licensed under [CC BY 4.0](LICENSE). Code (`scripts/`, `schema/`, `Makefile`, CI, `examples/impl-repo/`) is licensed under [Apache-2.0](LICENSE-CODE). Attribution: "mess.systems requirements (https://github.com/mess-systems/requirements), CC BY 4.0".
