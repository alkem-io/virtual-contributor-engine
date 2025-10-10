from time import time
from enum import Enum
from pydantic import Field
from .base import Base


class IngestionResult(Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class IngestWebsiteResult(Base):
    timestamp: int = Field(
        default_factory=lambda: int(time() * 1000), alias="timestamp"
    )
    result: IngestionResult = Field(
        default=IngestionResult.SUCCESS, alias="result"
    )
    error: str = Field(default="", alias="error")
