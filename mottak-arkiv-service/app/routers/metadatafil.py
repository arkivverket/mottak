from fastapi import APIRouter, status, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.domain.metadatafil_service import post_upload_metadatafil, get_metadatafil_get_content
from app.routers.dto.Metadatafil import Metadatafil
from app.routers.router_dependencies import get_db_session

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=Metadatafil,
             summary="Laste opp en metadatafil")
async def upload_metadatafil(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    return post_upload_metadatafil(file, db)


@router.get("/{id}/content",
             status_code=status.HTTP_200_OK,
             response_model=str,
             summary="Henter ut innehold(XML) fra en metadatafil")
async def upload_metadatafil(id: int, db: Session = Depends(get_db_session)):
    return get_metadatafil_get_content(id, db)
