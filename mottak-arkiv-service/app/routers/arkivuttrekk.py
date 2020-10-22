from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.arkivuttrekk_service import get_by_id, get_all
from app.routers.dto.Arkivuttrekk import Arkivuttrekk
from app.routers.router_dependencies import get_db_session

router = APIRouter()


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=Arkivuttrekk,
            summary="Hent arkivuttrekk basert på id")
async def router_get_by_id(id_: int, db: Session = Depends(get_db_session)):
    result = get_by_id(id_, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fant ikke Arkivuttrekk med id={id_}")
    return result


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Arkivuttrekk],
            summary="Hent alle arkivuttrekk")
async def router_get_all(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 10):
    return get_all(db, skip, limit)
