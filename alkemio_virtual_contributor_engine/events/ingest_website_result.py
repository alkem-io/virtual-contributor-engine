from time import time
from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict


class IngestionResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


@dataclass()
class IngestWebsiteResult:
    timestamp: int
    result: IngestionResult
    error: str

    def __init__(self, input_data: Dict[str, Any]) -> None:
        # timestamp is in milliseconds
        self.timestamp = input_data.get("timestamp", int(time() * 1000))
        self.result = input_data.get("result", IngestionResult.SUCCESS)
        self.error = input_data.get("error", "")

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "result": self.result.value,
            "error": self.error,
        }
