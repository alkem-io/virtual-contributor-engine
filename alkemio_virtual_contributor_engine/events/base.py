from pydantic import BaseModel

class Base(BaseModel):
    class Config:
        validate_by_name = True
        use_enum_values = True

    def dict(self, *args, **kwargs):
        if "by_alias" not in kwargs:
            kwargs["by_alias"] = True
        return super().dict(*args, **kwargs)
