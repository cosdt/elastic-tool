# escli_tool/cli.py

import argparse

from escli_tool.commands import create, delete, login, search, update


def main():
    parser = argparse.ArgumentParser(prog="escli", description="Elastic CLI 工具")
    subparsers = parser.add_subparsers(dest="command")

    # register subcommand
    create.register_subcommand(subparsers)
    search.register_subcommand(subparsers)
    login.register_subcommand(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
