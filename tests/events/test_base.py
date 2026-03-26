from pydantic import Field

from alkemio_virtual_contributor_engine.events.base import Base


class SampleModel(Base):
    name: str = Field(alias="displayName")
    age: int = Field(alias="userAge")


def test_model_dump_uses_aliases_by_default():
    m = SampleModel(displayName="Alice", userAge=30)
    dumped = m.model_dump()
    assert "displayName" in dumped
    assert "userAge" in dumped
    assert dumped["displayName"] == "Alice"


def test_model_dump_respects_explicit_by_alias_false():
    m = SampleModel(displayName="Alice", userAge=30)
    dumped = m.model_dump(by_alias=False)
    assert "name" in dumped
    assert "age" in dumped


def test_model_dump_by_alias_true_explicit():
    m = SampleModel(displayName="Alice", userAge=30)
    dumped = m.model_dump(by_alias=True)
    assert "displayName" in dumped
