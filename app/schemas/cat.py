from pydantic import BaseModel, Field, PositiveInt, condecimal

class CatCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    years_of_experience: PositiveInt
    breed: str = Field(min_length=1, max_length=120)
    salary: condecimal(gt=0, max_digits=12, decimal_places=2)

class CatUpdateSalary(BaseModel):
    salary: condecimal(gt=0, max_digits=12, decimal_places=2)

class CatOut(BaseModel):
    id: int
    name: str
    years_of_experience: int
    breed: str
    salary: float

    class Config:
        from_attributes = True
