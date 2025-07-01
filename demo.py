import json

from escli_tool.handler import DataHandler
from escli_tool.common import VLLM_SCHEMA_V1

def get_es_data():
    data_handler = DataHandler.maybe_from_env_or_keyring()
    records = []
    for _, data_tuple in VLLM_SCHEMA_V1.items():
        index_name, _ = data_tuple
        records.append(data_handler.search_data_from_vllm(index_name, source=True, size=1000))
    data_to_upload = set()
    
    for record in records:
        for hit in record['hits']['hits']:
            _source = hit.get('_source')
            if _source:
                commit_id = _source.get('commit_id')
                if commit_id == 'f04c6763d8b0a05905e241dfc7ea826a6b9cd587':
                    data_to_upload.add(hit['_id'])
                    print(_source)
                    print(hit)

    print(f"Data to upload: {data_to_upload}")
    # for _, data_tuple in VLLM_SCHEMA_V1.items():
    #     index_name, _ = data_tuple
    #     for _id in data_to_upload:
    #         data_handler.update_data_for_exist_id(index_name, _id, {"status": "error"})
if __name__ == '__main__':
    get_es_data()

