from dataclasses import dataclass
from typing import Any, Dict


@dataclass()
class IngestWebsite:
    base_url: str
    type: str
    purpose: str
    persona_service_id: str

    def __init__(self, input_data: Dict[str, Any]) -> None:
        print(input_data)
        self.base_url = input_data.get("baseUrl", "")
        self.type = input_data.get("type", "")
        self.purpose = input_data.get("purpose", "")
        self.persona_service_id = input_data.get("personaServiceId", "")

    def to_dict(self):
        return {
            "baseUrl": self.base_url,
            "type": self.type,
            "purpose": self.purpose,
            "personaServiceId": self.persona_service_id,
        }
