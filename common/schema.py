from typing import Annotated
from pydantic import BaseModel as PydanticModel, BeforeValidator


CoercedInt = Annotated[int, BeforeValidator(lambda val: int(val))]
CoercedIntNullable = Annotated[int | None, BeforeValidator(lambda val: None if val is None else int(val))]


class CustomBaseModel(PydanticModel):
    pass
