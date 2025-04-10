# escli_tool/commands/create.py
from escli_tool.handler import DataHandler
from escli_tool.utils import get_logger

logger = get_logger()


def register_subcommand(subparsers):
    parser = subparsers.add_parser(
        "delete", help="Delete a existed _id in the given index")
    parser.add_argument("--tag", default=None, help="Which version to save")
    parser.add_argument("--index", help="index name")
    parser.add_argument("--id",
                        help="IDs to delete (accepts multiple IDs)",
                        nargs="+")
    parser.set_defaults(func=run)


def run(args):
    """Delete a document from the given index and _id list. if no _id is provided, delete the index."""
    handler = DataHandler.maybe_from_env_or_keyring()
    index_name = args.index
    if args.tag:
        index_name = f"{index_name}_{args.tag}"
    handler.index_name = index_name
    id_to_delete = args.id
    if not id_to_delete:
        logger.info("No IDs provided for deletion. Deleting the index.")
        handler.delete_index(args.index)
    else:
        handler.delete_id_list_with_bulk_insert(id_to_delete)
