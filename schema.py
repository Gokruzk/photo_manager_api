from pydantic import BaseModel
from typing import Optional, TypeVar

T = TypeVar("T")


class ResponseSchema(BaseModel):
    status_code: int
    detail: str
    result: Optional[T] = None
