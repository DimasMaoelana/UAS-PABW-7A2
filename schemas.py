from pydantic import BaseModel

# Create ToDo Schema (Pydantic Model)
class CreateCars(BaseModel):
    id: int
    brand: str
    model: str
    price: int

# Complete ToDo Schema (Pydantic Model)
class Cars(BaseModel):
    id: int
    brand: str
    model: str
    price: int

    class Config:
        orm_mode = True