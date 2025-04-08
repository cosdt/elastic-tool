# escli_tool/commands/create.py
from argparse import _SubParsersAction

from escli_tool.handler import DataHandler
from escli_tool.utils import get_logger


logger = get_logger()

def register_subcommand(subparsers: _SubParsersAction):
    parser = subparsers.add_parser("search", help="search for an existed _id")
    parser.add_argument("--index", required=True, help="The index name to search")
    parser.add_argument("--source", action="store_true", help="Whether to expand details")
    parser.add_argument("--size", required=False, type=int, help="Size to search")
    parser.set_defaults(func=run)


def run(args):
    handler = DataHandler.maybe_from_env_or_keyring()
    res = handler.search_data_from_vllm(args.index, source=args.source)
    print(res)
    return res
