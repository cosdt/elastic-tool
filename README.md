# 🧰 elastic-tool

`elastic-tool` is a command line tool for interacting with [Elasticsearch](https://www.elastic.co/). It helps developers and data engineers to create, search, update, and delete indexes and documents via simple CLI commands.

---

## 📦 Installation

You can install the tool in **editable/development mode**:

```bash
git clone https://github.com/Potabk/elastic-tool.git
cd elastic-tool
pip install -e .
```
✅ After installation, the CLI command escli will be available in your terminal.

## Quick Start

✅ Check if CLI is available

```
escli --help
```

## Features
Create and delete Elasticsearch indexes

Insert, update, delete documents

Perform search queries (DSL or keyword-based)

Support both inline JSON and file-based input

Environment config via ES_OM_DOMAIN and ES_OM_AUTHORIZATION env vars