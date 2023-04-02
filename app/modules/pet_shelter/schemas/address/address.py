from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    id: int
    city: str
    country: str
    state: str
    street_address: Optional[str]
    zip_code: Optional[str]

    class Config:
        orm_mode = True

