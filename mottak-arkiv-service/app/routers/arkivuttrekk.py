from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app.domain.arkivuttrekk_service import get_by_id, get_all, create
from app.routers.dto.Arkivuttrekk import Arkivuttrekk, ArkivuttrekkBase
from app.routers.router_dependencies import get_db_session
from exceptions import MetadatafilNotFound, ArkivuttrekkNotFound, MetadatafilMissingInnhold

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=Arkivuttrekk,
             summary="Lagre et arkivuttrekk ut fra redigerbare felter")
def create_arkivuttrekk(arkivuttrekk: ArkivuttrekkBase, db: Session = Depends(get_db_session)):
    try:
        return create(arkivuttrekk, db)
    except MetadatafilNotFound or MetadatafilMissingInnhold as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)


@router.get("/{id}",
            status_code=status.HTTP_200_OK,
            response_model=Arkivuttrekk,
            summary="Hent arkivuttrekk basert på id")
async def router_get_by_id(id: int, db: Session = Depends(get_db_session)):
    try:
        return get_by_id(id, db)
    except ArkivuttrekkNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)


@router.get("",
            status_code=status.HTTP_200_OK,
            response_model=List[Arkivuttrekk],
            summary="Hent alle arkivuttrekk")
async def router_get_all(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 10):
    return get_all(db, skip, limit)
