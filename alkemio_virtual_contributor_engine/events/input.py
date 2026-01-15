from .base import Base
from enum import Enum
from typing import List, Optional
from pydantic import Field


class ResultHandlerAction(str, Enum):
    POST_REPLY = "postReply"
    POST_MESSAGE = "postMessage"
    NONE = "none"


class InvocationOperation(str, Enum):
    QUERY = "query"
    INGEST = "ingest"


class MessageSenderRole(str, Enum):
    HUMAN = "human"
    ASSISTANT = "assistant"


class ExternalMetadata(Base):
    """
    Represents external metadata for the input, specifically the
    thread identifier used in OpenAI's assistant API to track
    conversation threads.
    """
    thread_id: Optional[str] = Field(None, alias="threadId")


class ExternalConfig(Base):
    """
    Represents external configuration for the input, including API
    key, assistant ID, and model.
    """
    api_key: Optional[str] = Field(None, alias="apiKey")
    assistant_id: Optional[str] = Field(None, alias="assistantId")
    model: Optional[str] = Field(None, alias="model")


class HistoryItem(Base):
    content: str = Field(alias="content")
    role: MessageSenderRole = Field(alias="role")


class RoomDetails(Base):
    room_id: str = Field(alias="roomID")
    actor_id: str = Field(alias="actorId")
    thread_id: Optional[str] = Field(None, alias="threadID")
    vc_interaction_id: Optional[str] = Field(
        None, alias="vcInteractionID"
    )


class ResultHandler(Base):
    action: ResultHandlerAction = Field(alias="action")
    room_details: Optional[RoomDetails] = Field(
        None, alias="roomDetails"
    )


class Input(Base):
    engine: str = Field(alias="engine")
    operation: InvocationOperation = Field(
        InvocationOperation.QUERY, alias="operation"
    )
    user_id: str = Field(alias="userID")
    message: str = Field(alias="message")
    body_of_knowledge_id: str = Field(alias="bodyOfKnowledgeID")
    context_id: str = Field("", alias="contextID")
    history: List[HistoryItem] = Field(alias="history")
    external_metadata: Optional[ExternalMetadata] = Field(
        None, alias="externalMetadata"
    )
    external_config: Optional[ExternalConfig] = Field(
        None, alias="externalConfig"
    )
    display_name: str = Field(alias="displayName")
    description: str = Field("", alias="description")
    persona_id: str = Field(alias="personaID")
    language: Optional[str] = Field("EN", alias="language")
    result_handler: ResultHandler = Field(alias="resultHandler")
    prompt: Optional[List[str]] = Field(None, alias="prompt")
    prompt_graph: Optional[dict] = Field(
        None,
        alias="promptGraph",
        description="PromptGraph configuration parsed from JSON",
    )
