# escli_tool/commands/create.py
from argparse import _SubParsersAction

from escli_tool.handler import DataHandler


def register_subcommand(subparsers: _SubParsersAction):
    parser = subparsers.add_parser("update", help="Insert a new _id according to given index name")
    parser.add_argument("--index", required=True, help="Index name to insert")
    parser.add_argument("--size", required=False, type=int, help="查询的范围")
    parser.set_defaults(func=run)


def run(args):
    handler = DataHandler()
    res = handler.update_data_for_exist_id(args.index, source=args.source)
    print(res)
    return res
