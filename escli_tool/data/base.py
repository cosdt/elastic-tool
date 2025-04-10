from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, Union


@dataclass
class BaseDataEntry:
    commit_id: str
    commit_title: str
    test_name: str
    tp: int
    created_at: Union[str, None]
    model_name: str

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return asdict(self)
