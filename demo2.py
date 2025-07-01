import json

from escli_tool.handler import DataHandler
from escli_tool.common import VLLM_SCHEMA_V1

def get_es_data():
    data_handler = DataHandler.maybe_from_env_or_keyring()
    for _, data_tuple in VLLM_SCHEMA_V1.items():
        index_name, _ = data_tuple
        records = data_handler.search_data_from_vllm(index_name, source=True, size=1000)
    data_to_upload = set()
    for hit in records['hits']['hits']:
        _source = hit.get('_source')
        if _source:
            commit_id = _source.get('commit_id')
            if commit_id == '5177bef87a21331dcca11159d3d1438075cbd74e':
                data_to_upload.add(hit['_id'])
                print(_source)
                
    print(f"Data to upload: {data_to_upload}")
    # for _, data_tuple in VLLM_SCHEMA_V1.items():
    #     index_name, _ = data_tuple
    #     for _id in data_to_upload:
    #         data_handler.update_data_for_exist_id(index_name, _id, {"status": "error"})
if __name__ == '__main__':
    get_es_data()

