# 发布到 PyPI 指南

本文档说明如何将 `escli_tool` 发布到 [PyPI](https://pypi.org/)，包括一次性准备工作、打包流程、测试发布、正式发布，以及通过 GitHub Actions 自动化发布的推荐做法。

---

## 1. 前置准备（一次性）

### 1.1 注册账号

- 正式源：https://pypi.org/account/register/
- 测试源：https://test.pypi.org/account/register/（强烈建议先在这里演练一遍）

两个站点的账号是**独立**的，需要分别注册。

### 1.2 开启双因素认证（2FA）

登录后在 *Account settings* 里开启 2FA。2024 年之后 PyPI 已**强制要求**上传者开启 2FA，否则无法上传包。

### 1.3 创建 API Token

PyPI 已经废弃用户名/密码上传，必须使用 API Token。

1. 登录 PyPI → *Account settings* → *API tokens* → *Add API token*
2. 首次发布时 scope 选 **"Entire account"**（因为包还没创建，无法选特定项目）
3. 生成后的 token 形如 `pypi-AgEIcHlwaS5vcmc...`，**只显示一次**，务必复制保存
4. 包首次发布后，建议回到 PyPI **删除** Entire account token，重新创建一个 scope 限定到 `escli_tool` 项目的 token，最小权限原则

TestPyPI 同样操作一次，生成一个独立的 token。

### 1.4 本地工具链

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

## 4. 本地构建

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

### 本地校验

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

---

## 5. 先上传到 TestPyPI（强烈推荐）

TestPyPI 是一个完整的镜像站点，用于演练发布流程，不会污染正式源。

```bash
twine upload --repository testpypi dist/*
```

首次使用会要求输入：
- Username：`__token__`（字面量，不是你的用户名）
- Password：粘贴你的 TestPyPI API token（`pypi-...` 开头的那串）

或者在 `~/.pypirc` 配置：

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEI...（正式 token）

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEI...（测试 token）
```

> 注意：`~/.pypirc` 文件权限建议 `chmod 600`。

从 TestPyPI 验证安装：

```bash
pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  escli_tool
```

`--extra-index-url` 是必需的，因为 TestPyPI 上不一定有你的运行时依赖（如 `scipy`），要让 pip 能回退到正式源取依赖。

---

## 6. 正式发布到 PyPI

TestPyPI 流程走通后，上传到正式源：

```bash
twine upload dist/*
```

上传成功后：
- 包页面：`https://pypi.org/project/escli_tool/`
- 任何人都可以 `pip install escli_tool` 安装

⚠️ **PyPI 不允许删除或覆盖已发布的同版本号**。如果上传错了，只能在版本号上 `+1` 重新发布。最多可以 "yank"（隐藏）一个版本，但不能真正删除。

---

## 7. 发布后

```bash
# 推送 tag（如果之前没推）
git push origin vX.Y.Z

# 在 GitHub 上创建 Release，把 CHANGELOG 本次版本的条目粘进去作为 release notes
gh release create vX.Y.Z --title "vX.Y.Z" --notes-file <(sed -n '/## vX.Y.Z/,/## v/p' CHANGELOG.md)
```

---

## 8. 推荐：用 GitHub Actions 自动发布

手动 `twine upload` 容易出错、token 容易泄露。推荐用 GitHub Actions + **Trusted Publisher (OIDC)**，不用在仓库里存任何 token。

### 8.1 在 PyPI 配置 Trusted Publisher

登录 PyPI → 项目页 → *Settings* → *Publishing* → *Add a new publisher*：

- Owner：`Potabk`
- Repository name：`elastic-tool`
- Workflow name：`publish.yml`
- Environment name：`pypi`（可选，但建议）

### 8.2 添加 workflow 文件

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # setuptools-scm 需要完整历史读取 tag

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Build
        run: |
          python -m pip install --upgrade pip build
          python -m build

      - name: Check
        run: |
          pip install twine
          twine check dist/*

      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: pypi  # 对应 PyPI 上配置的 environment
    permissions:
      id-token: write  # OIDC 必需
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/

      - uses: pypa/gh-action-pypi-publish@release/v1
```

之后发布流程就是：

```bash
git tag v0.3.0
git push origin v0.3.0
# GitHub Actions 自动构建并发布，无需本地 twine
```

---

## 9. 常见问题

**Q: 上传时报 `File already exists`**
A: 同一版本号无法重新上传。改高版本号（比如打新的 git tag）重新构建。

**Q: `pip install` 装下来后 `escli` 命令找不到**
A: 检查 `setup.py` 的 `entry_points`，以及安装 Python 的 `Scripts`/`bin` 目录是否在 `$PATH` 中。

**Q: `setuptools-scm` 报 `LookupError: setuptools-scm was unable to detect version`**
A: 构建环境没有 git 历史或 tag。CI 里要用 `fetch-depth: 0`。

**Q: README 在 PyPI 页面渲染异常**
A: `twine check dist/*` 会在上传前捕获大部分问题。`long_description_content_type` 必须是 `text/markdown`。

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

---

## 10. 速查：一次标准发布流程

```bash
# 1. 确认干净、测试通过
git status
pytest

# 2. 更新 CHANGELOG.md 并提交
git add CHANGELOG.md && git commit -m "docs: changelog for v0.3.0"

# 3. 打 tag
git tag v0.3.0
git push origin main --tags

# 4a. 如果配置了 GitHub Actions Trusted Publisher：到这一步就完了，CI 会自动发布

# 4b. 手动发布：
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload --repository testpypi dist/*   # 先演练
twine upload dist/*                          # 正式发布
```
