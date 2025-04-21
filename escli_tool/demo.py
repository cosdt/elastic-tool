from escli_tool.handler import DataHandler


data_handler = DataHandler.maybe_from_env_or_keyring()
index_name = "vllm_benchmark_serving_testcli"
data_handler.index_name = index_name
res = data_handler.condition_search(index_name, 
                              conditions={"commit_id": "123456788"},
                             )
print(res)