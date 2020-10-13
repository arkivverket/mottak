from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.routers.dto.Arkivuttrekk import Arkivuttrekk
from app.routers.router_dependencies import get_db_session
from app.domain.arkivuttrekkservice import get_arkivuttrekk_get_by_id, get_arkivuttrekk_get_all

router = APIRouter()


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=Arkivuttrekk,
            summary="Hent arkivuttrekk basert på id")
async def get_by_id(id: int, db: Session = Depends(get_db_session)):
    return get_arkivuttrekk_get_by_id(id, db)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Arkivuttrekk],
            summary="Hent alle arkivuttrekk")
async def get_all(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 10):
    return get_arkivuttrekk_get_all(db, skip, limit)
