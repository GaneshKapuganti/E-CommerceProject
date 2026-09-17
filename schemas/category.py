from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)

class CategoryListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[CategoryResponse]