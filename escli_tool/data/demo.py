import os

from escli_tool.handler import DataHandler

domain = os.getenv("ES_OM_DOMAIN")
au = os.getenv("ES_OM_AUTHORIZATION")

data_handler = DataHandler(domain, au)
data = data_handler.search_data_from_vllm("vllm_benchmark_serving", source=True)
# print(data)
