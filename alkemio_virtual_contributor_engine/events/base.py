from pydantic import BaseModel, ConfigDict

class Base(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True,
    )

    def model_dump(self, *args, **kwargs):
        if "by_alias" not in kwargs:
            kwargs["by_alias"] = True
        return super().model_dump(*args, **kwargs)
