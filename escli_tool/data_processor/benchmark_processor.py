import json
import os
import re
import sys
from argparse import ArgumentParser
from calendar import c
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from sys import flags
from typing import Dict, List, Union

from escli_tool.registry import register_class
from escli_tool.data_processor.processor_base import ProcessorBase
from escli_tool.common import VLLM_SCHEMA
from escli_tool.utils import get_logger


logger = get_logger()

@dataclass
class BaseDataEntry:
    commit_id: str
    commit_title: str
    test_name: str
    tp: int
    created_at: Union[str, None]

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ServingDataEntry(BaseDataEntry):
    mean_ttft_ms: float
    median_ttft_ms: float
    p99_ttft_ms: float
    mean_tpot_ms: float
    p99_tpot_ms: float
    median_tpot_ms: float
    mean_itl_ms: float
    median_itl_ms: float
    p99_itl_ms: float
    request_rate: str
    request_throughput: float
    total_token_throughput: float


# Throughput
@dataclass
class ThroughputDataEntry(BaseDataEntry):
    requests_per_second: float
    tokens_per_second: float


# Latency
@dataclass
class LatencyDataEntry(BaseDataEntry):
    mean_latency: float
    median_latency: float
    percentile_99: float


@register_class
class BenchmarkProcessor(ProcessorBase):
    cls_name = 'benchmark'
    def __init__(self, commit_id: str, commit_title: str, created_at: str=None):
        super(ProcessorBase).__init__(commit_id, commit_title, created_at)
        self.schema: list = list(VLLM_SCHEMA)
        self.latency: LatencyDataEntry = None
        self.throughput: ThroughputDataEntry = None
        self.serving: ServingDataEntry = None
    
    @staticmethod
    def _read_from_json(folder_path: Union[str, Path]):
        res_map = {}
        for file_name in os.listdir(folder_path):
            if file_name.endswith("json"):
                file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)
                    res_map[Path(file_name).stem] = json_data
            except json.JSONDecodeError as e:
                logger.error(f"can not read from json: {file_name}")
                sys.exit(1)
        return res_map

    @staticmethod
    def _convert_s_ms(time_second: float) -> float:
        return round(time_second * 1000, 2)

    @classmethod
    def from_local_dir(cls, dir_path: str):
        res_map = cls._read_from_json(dir_path)

def get_project_root() -> Path:
    current_path = Path(__file__).resolve()
    while current_path != current_path.parent:
        if (current_path / ".git").exists() or (current_path / "setup.py").exists():
            return current_path
        current_path = current_path.parent
    return current_path




def extract_tp_value(s):
    match = re.search(r"tp(\d+)", s)
    return int(match.group(1)) if match else None


# def data_prc(
#     folder_path: Union[str, Path], commit_id, commit_title, created_at=None
# ) -> Dict[str, List[Union[ServingDataEntry, LatencyDataEntry, ThroughputDataEntry]]]:
#     commit_id = commit_id
#     commit_title = commit_title
#     json_data = read_from_json(folder_path)
#     res_instance = {
#         "vllm_benchmark_serving": [],
#         "vllm_benchmark_latency": [],
#         "vllm_benchmark_throughput": [],
#     }
#     for test_name, data in json_data.items():
#         test_prefix = str.split(test_name, "_")[0]
#         tp = extract_tp_value(test_name)
#         match test_prefix:
#             case "serving":
#                 res_instance["vllm_benchmark_serving"].append(
#                     ServingDataEntry(
#                         commit_id=commit_id,
#                         commit_title=commit_title,
#                         test_name=test_name,
#                         tp=tp,
#                         created_at=created_at,
#                         request_rate=data["request_rate"],
#                         mean_ttft_ms=data["mean_ttft_ms"],
#                         median_ttft_ms=data["median_ttft_ms"],
#                         p99_ttft_ms=data["p99_ttft_ms"],
#                         mean_itl_ms=data["mean_itl_ms"],
#                         median_itl_ms=data["median_itl_ms"],
#                         p99_itl_ms=data["p99_itl_ms"],
#                         mean_tpot_ms=data["mean_tpot_ms"],
#                         median_tpot_ms=data["median_tpot_ms"],
#                         p99_tpot_ms=data["p99_tpot_ms"],
#                     )
#                 )
#             case "latency":
#                 res_instance["vllm_benchmark_latency"].append(
#                     LatencyDataEntry(
#                         commit_id=commit_id,
#                         commit_title=commit_title,
#                         test_name=test_name,
#                         tp=tp,
#                         created_at=created_at,
#                         mean_latency=convert_s_ms(data["avg_latency"]),
#                         median_latency=convert_s_ms(data["percentiles"]["50"]),
#                         percentile_99=convert_s_ms(data["percentiles"]["99"]),
#                     )
#                 )
#             case "throughput":
#                 res_instance["vllm_benchmark_throughput"].append(
#                     ThroughputDataEntry(
#                         commit_id=commit_id,
#                         commit_title=commit_title,
#                         test_name=test_name,
#                         created_at=created_at,
#                         tp=tp,
#                         requests_per_second=data["requests_per_second"],
#                         tokens_per_second=data["tokens_per_second"],
#                     )
#                 )

#     return res_instance


def get_all_commit(file_path):
    res = {}
    with open(file_path, "r") as f:
        for line in f:
            commit = line.strip().split(" ", 1)
            commit_id, commit_title = commit[0], commit[1]
            res[commit_id] = commit_title
    return res
