from pydantic import BaseModel

from app.domain.models.Arkivkopi import ArkivkopiStatus


class Arkivkopi(BaseModel):
    """
    Used as the response model for GET "/arkivuttrekk/{id}/bestill_nedlasting/status"
    """
    id: int
    status: ArkivkopiStatus
    target_name: str

    class Config:
        orm_mode = True
