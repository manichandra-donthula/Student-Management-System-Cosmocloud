from pydantic import BaseModel

class AddressModel(BaseModel):
    city: str
    country: str

class StudentCreateModel(BaseModel):
    name: str
    age: int
    address: AddressModel

class StudentUpdateModel(BaseModel):
    name: str | None = None
    age: int | None = None
    address: AddressModel | None = None
