from abc import ABC, abstractmethod


class ProcessorBase(ABC):
    def __init__(self, commit_id: str, commit_title, created_at: str):
        self.commit_id = commit_id
        self.commit_title = commit_title
        self.created_at = created_at
    
    