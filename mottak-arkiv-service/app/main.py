#!/usr/bin/env python3

from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.db import get_session, repository
from app.dto.Arkivuttrekk import ArkivuttrekkOut

from dotenv import load_dotenv
load_dotenv()

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


# TODO Implementere helsesjekk av applikasjonen
@app.get("/health",
         status_code=status.HTTP_200_OK,
         tags=["health"],
         summary="Helsesjekk av applikasjonen")
async def health_check():
    return "Seems healthy"


@app.get("/arkiv/{uuid}",
         status_code=status.HTTP_200_OK,
         response_model=ArkivuttrekkOut,
         tags=["arkivuttrekk"],
         summary="Hent arkivuttrekk basert på objekt id(UUID)")
async def get_archive(uuid: UUID,  db: Session = Depends(get_db)):
    return repository.get_arkivuttrekk(db, uuid)


@app.get("/arkiver",
         status_code=status.HTTP_200_OK,
         response_model=List[ArkivuttrekkOut],
         tags=["arkivuttrekk"],
         summary="Hent alle arkivuttrekk")
def get_archives(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return repository.get_all_arkivuttrekk(db, skip, limit)


