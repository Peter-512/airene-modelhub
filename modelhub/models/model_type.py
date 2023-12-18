from typing import Literal

from pydantic import BaseModel


class ModelType(BaseModel):
    type: Literal["regressor", "classifier"]
