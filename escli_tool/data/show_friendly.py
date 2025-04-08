from typing import List, Optional

from escli_tool.handler import DataHandler
from escli_tool.data.common import VLLM_SCHEMA
from escli_tool.data.processor import (ServingDataEntry, 
                                       LatencyDataEntry, 
                                       ThroughputDataEntry, 
                                       BaseDataEntry)


def search_and_show(schema: List[str], tag: Optional[str], size: int):
    data_handler = DataHandler.maybe_from_env_or_keyring()
    for index in schema:
        # To add version control, a tag means which version should to search
        index = '_'.join(index, tag)
        _source = data_handler.search_data_from_vllm(index, source=True, size=size)
        print(_source)

