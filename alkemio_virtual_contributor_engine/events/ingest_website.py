from pydantic import Field
from .base import Base

class IngestWebsite(Base):
    base_url: str = Field(alias="baseUrl")
    type: str = Field(alias="type")
    purpose: str = Field(alias="purpose")
    persona_id: str = Field(alias="personaId")
