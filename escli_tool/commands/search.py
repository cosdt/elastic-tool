# escli_tool/commands/create.py
from argparse import _SubParsersAction
from email.policy import default

from escli_tool.handler import DataHandler
from escli_tool.utils import get_logger


logger = get_logger()

def register_subcommand(subparsers: _SubParsersAction):
    parser = subparsers.add_parser("search", help="search for an existed _id")
    parser.add_argument("--index", required=True, help="The index name to search")
    parser.add_argument("--source", action="store_true", help="Whether to expand details")
    parser.add_argument("--size", required=False, default=1000, type=int, help="Size to search")
    parser.add_argument("--tag", required=False, help="Which version to search")
    parser.set_defaults(func=run)


def run(args):
    """Search for an existed _id in the given index"""
    handler = DataHandler.maybe_from_env_or_keyring()
    index_name = args.index
    if args.tag:
        index_name = f"{index_name}_{args.tag}"
    res = handler.search_data_from_vllm(index_name, source=args.source, size=args.size)
    print(res)
    return res
