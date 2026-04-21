# 发布到 PyPI 指南

本文档说明如何将 `escli_tool` 发布到 [PyPI](https://pypi.org/)，包括一次性准备工作、本地手动发布流程，以及通过 GitHub Actions 在打 tag 后**自动构建并发布**的推荐做法。

---

## 1. 前置准备（一次性）

### 1.1 注册账号

https://pypi.org/account/register/

### 1.2 开启双因素认证（2FA）

登录后在 *Account settings* 里开启 2FA。2024 年之后 PyPI 已**强制要求**上传者开启 2FA，否则无法上传包。

### 1.3 创建 API Token（仅手动发布或首次发布需要）

PyPI 已经废弃用户名/密码上传，必须使用 API Token。

1. 登录 PyPI → *Account settings* → *API tokens* → *Add API token*
2. 首次发布时 scope 选 **"Entire account"**（因为包还没创建，无法选特定项目）
3. 生成后的 token 形如 `pypi-AgEIcHlwaS5vcmc...`，**只显示一次**，务必复制保存
4. 包首次发布后，建议回到 PyPI **删除** Entire account token，重新创建一个 scope 限定到 `escli_tool` 项目的 token，最小权限原则

> 推荐使用后文介绍的 GitHub Actions **Trusted Publisher (OIDC)** 方案，完全不需要长期保存 token。

### 1.4 本地工具链（仅本地手动发布需要）

```bash
python -m pip install --upgrade pip
python -m pip install --upgrade build twine setuptools-scm
```

- `build`：PEP 517 标准构建工具，生成 sdist 和 wheel
- `twine`：安全地把包上传到 PyPI
- `setuptools-scm`：本项目用它从 git tag 推导版本号

---

## 2. 发布前检查清单

每次发布前逐项确认：

- [ ] `README.md` 内容最新，能在 PyPI 页面正确渲染（long_description_content_type 已设为 `text/markdown`）
- [ ] `CHANGELOG.md` 已追加本次版本的变更说明
- [ ] `requirements.txt` 与 `pyproject.toml` 的依赖声明一致且最小化
- [ ] `escli_tool/data/` 下的数据文件（`*.json`、`*.txt`）若需随包分发，已通过 `package_data` 或 `MANIFEST.in` 包含
- [ ] 工作区干净（`git status` 无未提交改动）
- [ ] 所有测试通过（`pytest`）
- [ ] Lint/格式检查通过（`bash tools/format.sh` 或 CI 要求的命令）
- [ ] 打好了 git tag，格式为 `vX.Y.Z`（本项目使用 `setuptools-scm`，版本号**来自 tag**）

---

## 3. 版本号管理

本项目使用 `setuptools-scm`：版本号**自动来自 git tag**，不需要在任何文件里手写版本号。

```bash
# 查看当前仓库会被识别为什么版本
python -m setuptools_scm

# 发布新版本前，打好 tag
git tag v0.3.0
git push origin v0.3.0
```

规则：
- 在 tag 所在 commit 上构建 → 版本 `0.3.0`
- 在 tag 之后的 commit 上构建 → 版本带 dev 后缀，如 `0.3.1.dev3+g1a2b3c4`（不能上传到 PyPI 正式源）

遵循 [语义化版本 SemVer](https://semver.org/lang/zh-CN/)：
- `MAJOR`（大版本）：不兼容的 API 变更
- `MINOR`（小版本）：向下兼容的新功能
- `PATCH`（补丁）：向下兼容的 bug 修复

---

## 4. 本地手动发布（备选方案）

> 推荐优先使用 [§6 GitHub Actions 自动发布](#6-推荐打-tag-后用-github-actions-自动发布)，本节只作为手动操作的备份方案保留。

### 4.1 构建

在项目根执行：

```bash
# 清理旧构建产物（重要，避免上传到旧 artifacts）
rm -rf dist/ build/ *.egg-info escli_tool.egg-info

# 构建 sdist + wheel
python -m build
```

成功后 `dist/` 下会生成两个文件：

```
dist/
├── escli_tool-0.3.0-py3-none-any.whl     # wheel（二进制分发）
└── escli_tool-0.3.0.tar.gz                # sdist（源码分发）
```

### 4.2 本地校验

```bash
# 静态检查元数据和 README 渲染
twine check dist/*

# 在干净的虚拟环境里试装，验证 entry_point 可用
python -m venv /tmp/verify-escli
source /tmp/verify-escli/bin/activate
pip install dist/escli_tool-*.whl
escli --help
deactivate && rm -rf /tmp/verify-escli
```

`twine check` 必须全部 `PASSED` 才能继续。

### 4.3 上传

```bash
twine upload dist/*
```

首次使用会要求输入：
- Username：`__token__`（字面量，不是你的用户名）
- Password：粘贴你的 PyPI API token（`pypi-...` 开头的那串）

或在 `~/.pypirc` 中配置（注意 `chmod 600`）：

```ini
[pypi]
username = __token__
password = pypi-AgEI...
```

---

## 5. 发布后

```bash
# 推送 tag（如果之前没推）
git push origin vX.Y.Z

# 在 GitHub 上创建 Release，把 CHANGELOG 本次版本的条目粘进去作为 release notes
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <(sed -n '/## vX.Y.Z/,/## v/p' CHANGELOG.md)
```

⚠️ **PyPI 不允许删除或覆盖已发布的同版本号**。如果上传错了，只能在版本号上 `+1` 重新发布。最多可以 "yank"（隐藏）一个版本，但不能真正删除。

---

## 6. 推荐：打 tag 后用 GitHub Actions 自动发布

这是本项目**推荐的发布方式**。配置完成后，开发者只需要：

```bash
git tag v0.3.0
git push origin v0.3.0
```

GitHub Actions 就会自动构建 wheel/sdist、做元数据校验、上传到 PyPI、创建 GitHub Release。**不需要本地装 build/twine，也不需要在仓库里保存任何 token。**

### 6.1 工作机制概览

```
  开发者                GitHub                         PyPI
    │                     │                             │
    │ git push --tags     │                             │
    ├────────────────────▶│                             │
    │                     │ 触发 workflow               │
    │                     │   ├─ build (sdist+wheel)    │
    │                     │   ├─ twine check            │
    │                     │   └─ OIDC 换取一次性 token ─▶│
    │                     │          upload ───────────▶│
    │                     │                             │ ✅ published
    │                     │ 创建 GitHub Release         │
```

核心是 **Trusted Publisher (OIDC)**：PyPI 和 GitHub 之间通过 OpenID Connect 建立信任，每次发布由 PyPI 签发一个仅在本次流程中有效的一次性 token，比长期 token 更安全。

### 6.2 在 PyPI 配置 Trusted Publisher

> 首次发布（PyPI 上还没有该项目）和后续发布的配置入口不同，分别说明。

#### 情况 A：项目**已经存在**于 PyPI（后续发布）

登录 PyPI → 你的项目 `escli_tool` → *Manage* → *Publishing* → *Add a new publisher*，填入：

| 字段 | 值 |
| --- | --- |
| Owner | `Potabk` |
| Repository name | `elastic-tool` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

#### 情况 B：项目**还没发布过**（首次发布）

有两种选择：

1. **先手动发布一次 0.0.1**：按 [§4 本地手动发布](#4-本地手动发布备选方案) 走一次，之后按情况 A 配置 Trusted Publisher
2. **直接用 Pending Publisher**：PyPI → *Account settings* → *Publishing* → *Add a pending publisher*，`Project name` 填 `escli_tool`，其它字段同上。打 tag 触发 workflow 后，PyPI 会在本次上传时自动创建项目并绑定 publisher

### 6.3 在 GitHub 仓库配置 Environment（可选但推荐）

Environment 用于在发布前加一层人工审批和保护规则：

1. GitHub 仓库 → *Settings* → *Environments* → *New environment*
2. 名字填 `pypi`（与 PyPI 上配置的 Environment name 保持一致）
3. 可选开启：
   - **Required reviewers**：发布前需要指定的人手动点 *Approve*
   - **Deployment branches and tags** → *Selected tags* → 添加 `v*`，保证只有以 `v` 开头的 tag 才能触发发布

### 6.4 创建 workflow 文件

在 [.github/workflows/publish.yml](.github/workflows/publish.yml) 放入：

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read

jobs:
  build:
    name: Build distributions
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          # setuptools-scm 需要完整历史 + tag 才能推导版本号
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install build tooling
        run: python -m pip install --upgrade pip build twine

      - name: Build sdist and wheel
        run: python -m build

      - name: Validate distributions
        run: python -m twine check --strict dist/*

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          if-no-files-found: error

  publish-pypi:
    name: Publish to PyPI
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: pypi
      url: https://pypi.org/project/escli_tool/
    permissions:
      id-token: write  # OIDC 签发一次性 token，必需
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1

  github-release:
    name: Create GitHub Release
    needs: publish-pypi
    runs-on: ubuntu-latest
    permissions:
      contents: write  # 创建 release 需要
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh release create "${GITHUB_REF_NAME}" \
            --title "${GITHUB_REF_NAME}" \
            --generate-notes \
            dist/*
```

说明：
- **触发条件**：只在推送形如 `v*` 的 tag 时触发，不会被普通 push 误触发
- **三段式 job**：`build` → `publish-pypi` → `github-release`，任一步失败不会污染后续
- `build` 里做了 `twine check --strict`，提前拦截 README 渲染问题
- `publish-pypi` 的 `environment: pypi` 让这个 job 受 Environment 保护规则约束（结合 §6.3 的 Required reviewers 就能做人工审批）
- `id-token: write` 是 OIDC 的硬性要求，没有这个权限就拿不到 token
- `github-release` 自动创建 GitHub Release 并附上 wheel/sdist，`--generate-notes` 会根据 PR 自动生成 release notes

### 6.5 完整发布流程（自动化路径）

```bash
# 1. 更新 CHANGELOG.md，提交
vim CHANGELOG.md
git add CHANGELOG.md
git commit -m "docs: changelog for v0.3.0"
git push origin main

# 2. 打 tag 并推送 —— 到这一步就完了
git tag v0.3.0
git push origin v0.3.0

# 3. 去 GitHub Actions 页面看 workflow 运行
#    若配置了 Required reviewers，publish-pypi job 会停在 "Waiting" 等审批
```

完成后在 https://pypi.org/project/escli_tool/ 可见新版本。

### 6.6 如果 workflow 失败了怎么办

- **build 阶段失败**：通常是代码或依赖问题，修好后把 tag 重新指向新 commit：
  ```bash
  git tag -d v0.3.0
  git push origin :refs/tags/v0.3.0   # 删掉远程 tag
  # 修复、提交
  git tag v0.3.0
  git push origin v0.3.0
  ```
- **publish-pypi 阶段失败（如版本已存在）**：改版本号重来，不能覆盖：
  ```bash
  git tag v0.3.1
  git push origin v0.3.1
  ```
- **OIDC 报 `invalid-publisher`**：检查 PyPI Trusted Publisher 配置的 `Workflow name` 是否精确等于 `publish.yml`、`Environment name` 是否和 workflow 里的 `environment: pypi` 一致

---

## 7. 常见问题

**Q: 上传时报 `File already exists`**
A: 同一版本号无法重新上传。打一个更高版本号的 tag 重来。

**Q: `pip install` 装下来后 `escli` 命令找不到**
A: 检查 `setup.py` 的 `entry_points`，以及安装 Python 的 `Scripts`/`bin` 目录是否在 `$PATH` 中。

**Q: `setuptools-scm` 报 `LookupError: setuptools-scm was unable to detect version`**
A: 构建环境没有 git 历史或 tag。CI 里一定要 `fetch-depth: 0`。

**Q: README 在 PyPI 页面渲染异常**
A: `twine check --strict dist/*` 在上传前可以捕获大部分问题。`long_description_content_type` 必须是 `text/markdown`。

**Q: 包里缺了 `escli_tool/data/*.json`**
A: 非 `.py` 文件默认不会打进 wheel。在 `setup()` 里加：
```python
include_package_data=True,
package_data={"escli_tool": ["data/*.json", "data/*.txt"]},
```
同时在项目根创建 `MANIFEST.in`：
```
include README.md LICENSE CHANGELOG.md
recursive-include escli_tool/data *.json *.txt
```

**Q: 打 tag 后 workflow 没有被触发**
A: 确认推送时带上了 tag（`git push origin v0.3.0` 或 `git push --tags`）。普通 `git push` 不会推送 tag。
