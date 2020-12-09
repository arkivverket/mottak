from pydantic import BaseModel
from uuid import UUID

class SASToken(BaseModel):
    """ DTO for the generate_sas endpoint."""
    status: int

    class Config:
        orm_mode = True
