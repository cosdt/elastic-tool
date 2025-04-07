# escli_tool/commands/create.py

import json
import os

from escli_tool.handler import DataHandler


def register_subcommand(subparsers):
    parser = subparsers.add_parser("create", help="创建索引或插入文档")
    parser.add_argument("--index", required=True, help="索引名称")
    parser.add_argument("--mapping", help="创建索引的字段映射(json 字符串或文件)")
    parser.add_argument("--doc", help="插入文档(json 字符串或文件)")
    parser.set_defaults(func=run)

def run(args):
    handler = DataHandler()
    handler.index_name = args.index

    if args.mapping:
        mapping = _load_json(args.mapping)
        handler.create_table_with_property_type(mapping)

    if args.doc:
        doc = _load_json(args.doc)
        handler.insert_document(doc)

def _load_json(content):
    if os.path.exists(content):
        with open(content) as f:
            return json.load(f)
    return json.loads(content)
