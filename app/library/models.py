from pydantic_mongo import ObjectIdField
from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    id: ObjectIdField = Field(default_factory=ObjectIdField, alias="_id")
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
