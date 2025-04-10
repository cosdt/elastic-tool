# escli_tool/commands/create.py
from escli_tool.registry import get_class


def register_subcommand(subparsers):
    parser = subparsers.add_parser("add",
                                   help="Insert a new _id in the given index")
    parser.add_argument("--tag", default=None, help="Which version to save")
    parser.add_argument("--res_dir",
                        help="Result dir which include json files")
    parser.add_argument("--processor",
                        help="Processor selected to process json files")
    parser.add_argument("--commit_id", help="Commit hash")
    parser.add_argument("--commit_title", help="Commit massage")
    parser.add_argument("--model_name", help="Model test on")
    parser.add_argument("--created_at",
                        help="What time current commit is submitted")
    parser.set_defaults(func=run)


def run(args):
    """
    Insert a document loading from local dir, need to provide a processor to process the specific data.
    For example, if you want to insert performance benchmark result(which saved as json files), you need
    to provide a benchmark processor to process the json files. and the processor should process the data
    into a data format that es can accept.
    If the processor is not provided, the default processor will be used.
    """
    processor_name = args.processor
    if not processor_name:
        # Set default processor to benchmark
        processor_name = 'benchmark'
    # TODO: do not only read data from local dir, but also read dict user customized
    if not args.res_dir:
        raise ValueError("Result dir is required")

    processor = get_class(processor_name)(
        args.commit_id,
        args.commit_title,
        args.created_at,
        args.model_name,
        args.tag,
    )
    processor.send_to_es(args.res_dir, )
