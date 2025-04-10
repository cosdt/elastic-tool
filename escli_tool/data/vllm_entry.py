from dataclasses import dataclass, field

from escli_tool.data.base import BaseDataEntry


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
    model_id: str
    model_name: str= field(init=False)

    def __post_init__(self):
        # Serving results do not have field model_name, for backward compatibility
        # we set model_id to model_name
        super().__post_init__()
        self.model_name = self.model_id
        self.model_id = self.model_id.split("/")[-1]
        self.model_name = self.model_name.split("/")[-1]

# Throughput
@dataclass
class ThroughputDataEntry(BaseDataEntry):
    requests_per_second: float
    tokens_per_second: float
    model_name: str

    def __post_init__(self):
        super().__post_init__()
        self.model_name = self.model_name.split("/")[-1]

# Latency
@dataclass
class LatencyDataEntry(BaseDataEntry):
    avg_latency: float
    percentiles: dict[str, float]
    model_name: str
    mean_latency: float = field(init=False)
    median_latency: float = field(init=False)
    percentile_99: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        # Convert all latency values from seconds to milliseconds
        self.percentiles = {
            k: convert_s_ms(v)
            for k, v in self.percentiles.items()
        }
        self.avg_latency = convert_s_ms(self.avg_latency)
        self.mean_latency = self.avg_latency
        if not isinstance(self.percentiles, dict):
            raise ValueError("percentiles must be a dictionary")
        if "50" not in self.percentiles or "99" not in self.percentiles:
            raise ValueError("percentiles must contain keys '50' and '99'")
        self.median_latency = self.percentiles["50"]
        self.percentile_99 = self.percentiles["99"]
        self.model_name = self.model_name.split("/")[-1]


def convert_s_ms(time_second: float) -> float:
    return round(time_second * 1000, 2)
