import os
import json
from escli_tool.processor.benchmark_processor import BenchmarkProcessor

def read_from_file():
    with open("./commit_log.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        res = []
        for line in lines:
            commit_id, commit_title = line.strip().split(" ", 1)
            res.append((commit_id, commit_title))

    return res

from escli_tool.handler import DataHandler

def process_data(date_list: list[str, str]):
    handler = DataHandler.maybe_from_env_or_keyring() 
    processor_list = []
    for commit_id, commit_title in date_list:
        pass
        
    

if __name__ == '__main__':
    res = read_from_file()
    print(res)
    print(f"Total commits: {len(res)}")
    handler = DataHandler.maybe_from_env_or_keyring() 
