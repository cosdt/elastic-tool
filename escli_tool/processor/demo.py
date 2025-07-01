import json

from escli_tool.handler import DataHandler
from escli_tool.common import VLLM_SCHEMA_V1

def get_es_data():
    data_handler = DataHandler.maybe_from_env_or_keyring()
    for _, data_tuple in VLLM_SCHEMA_V1.items():
        index_name, _ = data_tuple
        records = data_handler.search_data_from_vllm(index_name, source=True, size=1000)
    commit_ids = set()
    data_to_upload = []
    for hit in records['hits']['hits']:
        _source = hit.get('_source')
        if _source:
            commit_id = _source.get('commit_id')
            status = _source.get('status', 'normal')
            extra_feat = _source.get('extra_features', None)
            if extra_feat:
                use_v1 = extra_feat.get('VLLM_USE_V1', '0')
                if use_v1 == '1':
                    print(_source)
                    _source["status"] = 'error'
                    commit_ids.add(commit_id)
    data_handler.update_data_for_exist_id()
    print(f"Total records with VLLM_USE_V1=1: {len(commit_ids)}")
if __name__ == '__main__':
    get_es_data()
