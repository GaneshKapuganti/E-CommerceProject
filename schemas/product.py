from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    price: float
    stock_quantity: int


class ProductPatch(BaseModel):
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None


class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    description: str | None = None
    price: float
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[ProductResponse]