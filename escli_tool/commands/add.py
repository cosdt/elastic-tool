# escli_tool/commands/create.py
from email.policy import default
import json
import os

from escli_tool.handler import DataHandler


def register_subcommand(subparsers):
    parser = subparsers.add_parser("add", help="Insert a new _id in the given index")
    # parser.add_argument("--index", required=True, help="Index name")
    parser.add_argument("--tag", default=None, help="Which version to save")
    parser.add_argument("--res_dir", help="Result dir which include json files")
    parser.add_argument("--processor", help="Processor selected to process json files")
    parser.set_defaults(func=run)


def run(args):
    handler = DataHandler.maybe_from_env_or_keyring()
    handler.index_name = args.index

    if args.mapping:
        mapping = _load_json(args.mapping)
        handler.add_single_data(mapping)

    if args.doc:
        doc = _load_json(args.doc)
        handler.insert_document(doc)


def _load_json(content):
    if os.path.exists(content):
        with open(content) as f:
            return json.load(f)
    return json.loads(content)
