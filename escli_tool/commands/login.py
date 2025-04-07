from escli_tool.handler import DataHandler
from escli_tool.utils import get_logger, save_credentials

logger = get_logger()

def register_subcommand(subparsers):
    parser = subparsers.add_parser("login", help="登录到 Elastic 服务")
    parser.add_argument("--domain", required=True, help="Elasticsearch 域名（例如 http://localhost:9200）")
    parser.add_argument("--token", required=True, help="用于 Authorization 的 Token")
    parser.set_defaults(func=run)


def run(args):
    try:
        DataHandler(args.domain, args.token)
        save_credentials(args.domain, args.token)
        logger.info("✅ login successful")
    except ConnectionError as e:
        logger.error(f"❌ login error: {e}")
