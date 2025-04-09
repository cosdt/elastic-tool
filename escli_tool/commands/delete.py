# escli_tool/commands/create.py
from email.policy import default
import json
import os

from escli_tool.handler import DataHandler
from escli_tool.registry import  get_class


def register_subcommand(subparsers):
    parser = subparsers.add_parser("delete", help="Delete a existed _id in the given index")
    parser.add_argument("--tag", default=None, help="Which version to save")
    parser.add_argument("--index", help="index name")
    parser.add_argument("--id", help="IDs to delete (accepts multiple IDs)", nargs="+")
    parser.set_defaults(func=run)


def run(args):
    handler = DataHandler.maybe_from_env_or_keyring()
    handler.index_name = args.index
    id_to_delete = args.id
    if not id_to_delete:
        raise ValueError("Please provide at least one ID to delete.")
    handler.delete_id_list_with_bulk_insert(id_to_delete)
