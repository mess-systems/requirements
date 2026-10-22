[English](README.md) | [Русский](README.ru.md) | **简体中文**

# mess.systems requirements：需求即代码

用代码方式管理需求的模板：在 git 中使用带 YAML front matter 的 Markdown，在 CI 中校验，自动生成需求登记表，配合 ADR，通过 [OpenFastTrace](https://github.com/itsallcode/openfasttrace)（OFT）追溯到代码，用 MkDocs 生成站点，并提供面向 AI 智能体的规则和提示词。示例描述的是虚构公司 mess.systems 的虚构产品 **x**。

示例、提示词和流程文档的工作语言是俄语。本 README 和英文 README 介绍整个包，内容本身尚未翻译。

## 快速开始
```bash
python3 -m pip install -r requirements-dev.txt
$EDITOR reqs.config.yaml        # 前缀、类型、范围
make check                      # 校验并检查 REGISTER.md 是否最新
make trace IMPL=../my-service   # 需要 oft（OpenFastTrace 4.11）或 Java 21 加 jar；TRACE_STRICT=1 时有缺陷即失败
python3 -m pip install -r requirements-docs.txt && make site
```

## 原则
1. 一个文件对应一条需求，文件名即 ID，目录即范围。
2. 前缀、类型、范围和状态写在 `reqs.config.yaml` 中，而不是代码里。
3. 每条需求都有验收标准和 OFT 标记 `req~ID~N`。
4. 代码中用 `[impl->req~ID~1]`，测试中用 `[utest->req~ID~1]` 或 `[itest->req~ID~1]`。
5. 登记表自动生成，不手工修改，CI 检查其是否最新。
6. `approved` 和 `verified` 状态只能通过经人工批准的 PR 设置。
7. 严格程度分阶段提高：先警告，修复后再设为错误。
8. 不含敏感信息：没有密钥、个人数据、人名或内部地址。

## 与 mess.systems 其他仓库的关系

| 仓库 | 提供什么 |
|---|---|
| [naming-standard](https://github.com/mess-systems/naming-standard) | 产品、域、环境、负责人以及验收标准中资源的命名，见 [docs/naming-standard.md](docs/naming-standard.md) |
| [tech-radar](https://github.com/mess-systems/tech-radar) | 本包使用的工具：OpenFastTrace、MkDocs Material、GitHub Actions、Forgejo Actions |
| [blueprints](https://github.com/mess-systems/blueprints) | 参考架构；其需求可以用本包管理 |

## 许可

文本（文档、需求、ADR、提示词）采用 [CC BY 4.0](LICENSE)。代码（`scripts/`、`schema/`、`Makefile`、CI、`examples/impl-repo/`）采用 [Apache-2.0](LICENSE-CODE)。署名："mess.systems requirements (https://github.com/mess-systems/requirements), CC BY 4.0"。
