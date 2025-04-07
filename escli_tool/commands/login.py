from escli_tool.handler import DataHandler
from escli_tool.config import save_config


def register_subcommand(subparsers):
    parser = subparsers.add_parser("login", help="登录到 Elastic 服务")
    parser.add_argument("--domain", required=True, help="Elasticsearch 域名（例如 http://localhost:9200）")
    parser.add_argument("--token", required=True, help="用于 Authorization 的 Token")
    parser.set_defaults(func=run)


def run(args):
    save_config(args.domain, args.token)
    print("✅ 登录成功，配置已保存至 ~/.escli/config.json")
