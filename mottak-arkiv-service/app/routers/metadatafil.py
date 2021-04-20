from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.exceptions import InvalidContentType, MetadatafilNotFound
from app.routers.dto.Metadata import Metadata
from app.routers.dto.Metadatafil import Metadatafil
from app.routers.mappers.metadafil import to_metadata
from app.routers.router_dependencies import get_db_session
from app.routers.services.metadatafil_service import get_content, get_metadatafil, upload_metadatafil

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=Metadatafil,
             summary="Laste opp en metadatafil")
async def router_upload_metadatafil(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    try:
        return upload_metadatafil(file, db)
    except InvalidContentType as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)


@router.get("/{id}/content",
            status_code=status.HTTP_200_OK,
            response_model=str,
            summary="Henter ut innehold(XML) fra en metadatafil")
async def router_get_content(metadatafil_id: int, db: Session = Depends(get_db_session)):
    try:
        return Response(content=get_content(metadatafil_id, db), media_type="application/xml")
    except MetadatafilNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)


@router.get("/{metadatafil_id}/parsed",
            status_code=status.HTTP_200_OK,
            response_model=Metadata,
            summary="Henter ut parset innehold(XML) fra en metadatafil")
async def router_get_parsed_content(metadatafil_id: int, db: Session = Depends(get_db_session)):
    try:
        metadatafil = get_metadatafil(metadatafil_id, db)
        metadata = to_metadata(metadatafil)
        return metadata
    except MetadatafilNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
