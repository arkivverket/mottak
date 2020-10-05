#!/usr/bin/env python3
from typing import List
from fastapi import FastAPI, Depends, Request, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, exc
from app.db.database import get_session
from app.db.repository import get_arkivuttrekk, get_all_arkivuttrekk, create_metadatafil
from app.dto.Arkivuttrekk import Arkivuttrekk
from app.dto.Metadatafil import BaseMetadatafil, Metadatafil

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass

app = FastAPI(
    title="Mottak-arkiv-service",
    description="En tjeneste for mottak av arkiver",
    version="0.1.0"
)


# Depdendency
def get_db():
    try:
        db = get_session()
        yield db
    finally:
        db.close()


@app.exception_handler(exc.NoResultFound)
async def sqlalchemy_exception_handler(request: Request, exception: exc.NoResultFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder(
            {"message": f"Could not find element with id {request.path_params['id']}", "exception": exception})
    )


# TODO Implementere helsesjekk av applikasjonen
@app.get("/health",
         status_code=status.HTTP_200_OK,
         tags=["health"],
         summary="Helsesjekk av applikasjonen")
async def health_check():
    return "Seems healthy"


@app.post("/metadatafil",
          status_code=status.HTTP_201_CREATED,
          response_model=Metadatafil,
          tags=["metadata"],
          summary="Laste opp en metadatafil")
async def upload_metadatafil(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read file content (XML) as utf-8 and remove newlines
    xmlstring = file.file.read().decode('utf-8').replace('\r\n', '')
    metadatafil = BaseMetadatafil(file.filename, file.content_type, xmlstring)
    return create_metadatafil(db, metadatafil)


@app.get("/arkivuttrekk/{id}",
         status_code=status.HTTP_200_OK,
         response_model=Arkivuttrekk,
         tags=["arkivuttrekk"],
         summary="Hent arkivuttrekk basert på id")
async def get_archive(id: int,  db: Session = Depends(get_db)):
    return get_arkivuttrekk(db, id)


@app.get("/arkivuttrekk",
         status_code=status.HTTP_200_OK,
         response_model=List[Arkivuttrekk],
         tags=["arkivuttrekk"],
         summary="Hent alle arkivuttrekk")
async def get_archives(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_all_arkivuttrekk(db, skip, limit)


