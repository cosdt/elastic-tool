import os
import json
from pathlib import Path
import re
from typing import Union


def read_from_json(file_path: Union[str, Path]):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data