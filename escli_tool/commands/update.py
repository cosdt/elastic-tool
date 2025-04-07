# escli_tool/commands/create.py
from argparse import _SubParsersAction

from escli_tool.handler import DataHandler


def register_subcommand(subparsers: _SubParsersAction):
    parser = subparsers.add_parser("update", help="根据index更新已有的doc")
    parser.add_argument("--index", required=True, help="索引名称")
    parser.add_argument("--source", action='store_true',  help="是否展开详细的文档")
    parser.add_argument("--size", required=False, type=int, help="查询的范围")
    parser.set_defaults(func=run)

def run(args):
    handler = DataHandler()
    res = handler.update_data_for_exist_id(args.index, source=args.source)
    print(res)
    return res
