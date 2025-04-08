import json

from escli_tool.handler import DataHandler


file_path = './res/serving_llama8B_tp1_qps_inf.json'

with open(file_path, 'r') as f:
    data = json.load(f)

for k, v in data.items():
    if k == 'total_token_throughput':
        print(v)