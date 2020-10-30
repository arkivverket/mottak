from fastapi import APIRouter, status, Depends, UploadFile, File, HTTPException, Response
from sqlalchemy.orm import Session

from app.domain.metadatafil_service import upload_metadatafil, get_content, get_parsed_content
from app.routers.dto.Metadatafil import Metadatafil
from app.routers.router_dependencies import get_db_session
from app.routers.dto.Arkivuttrekk import ArkivuttrekkBase
from app.exceptions import MetadatafilNotFound

router = APIRouter()


@router.post("",
             status_code=status.HTTP_201_CREATED,
             response_model=Metadatafil,
             summary="Laste opp en metadatafil")
async def router_upload_metadatafil(file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    return upload_metadatafil(file, db)


@router.get("/{id}/content",
            status_code=status.HTTP_200_OK,
            response_model=str,
            summary="Henter ut innehold(XML) fra en metadatafil")
async def router_get_content(id: int, db: Session = Depends(get_db_session)):
    try:
        return Response(content=get_content(id, db), media_type="application/xml")
    except MetadatafilNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
    # result = Response(content=get_content(id, db), media_type="application/xml")
    # if result is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fant ikke Metadatafil med id={id}")
    # return result


@router.get("/{id}/parsed",
            status_code=status.HTTP_200_OK,
            response_model=ArkivuttrekkBase,
            summary="Henter ut parset innehold(XML) fra en metadatafil")
async def router_get_parsed_content(id: int, db: Session = Depends(get_db_session)):
    try:
        return get_parsed_content(id, db)
    except MetadatafilNotFound as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err.message)
    # result = get_parsed_content(id, db)
    # if result is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fant ikke Metadatafil med id={id}")
    # return result
