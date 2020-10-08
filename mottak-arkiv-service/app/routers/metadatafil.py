from fastapi import APIRouter, status, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.routers.dto.Metadatafil import Metadatafil
from app.routers.router_dependencies import get_db_session
from app.services.routerservice import post_upload_metadatafil

router = APIRouter()


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=Metadatafil,
             summary="Laste opp en metadatafil")
async def upload_metadatafil(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    return post_upload_metadatafil(file, db)
