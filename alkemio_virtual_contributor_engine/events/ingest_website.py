from enum import Enum
from pydantic import Field
from .base import Base


class SummarizationModel(str, Enum):
    MISTRAL_MEDIUM = "mistral-medium"
    MISTRAL_LARGE = "mistral-large"


class IngestWebsite(Base):
    base_url: str = Field(alias="baseUrl")
    type: str = Field(alias="type")
    purpose: str = Field(alias="purpose")
    persona_id: str = Field(alias="personaId")
    summarization_model: SummarizationModel = Field(
        default=SummarizationModel.MISTRAL_MEDIUM,
        alias="summarizationModel"
    )
