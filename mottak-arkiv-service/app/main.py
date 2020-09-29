#!/usr/bin/env python3

from typing import List
from uuid import UUID
from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.db.repository import get_arkivuttrekk, get_all_arkivuttrekk
from app.dto.Arkivuttrekk import Arkivuttrekk

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


# TODO Implementere helsesjekk av applikasjonen
@app.get("/health",
         status_code=status.HTTP_200_OK,
         tags=["health"],
         summary="Helsesjekk av applikasjonen")
async def health_check():
    return "Seems healthy"


@app.get("/arkiv/{uuid}",
         status_code=status.HTTP_200_OK,
         response_model=Arkivuttrekk,
         tags=["arkivuttrekk"],
         summary="Hent arkivuttrekk basert på objekt id(UUID)")
async def get_archive(uuid: UUID,  db: Session = Depends(get_db)):
    return get_arkivuttrekk(db, uuid)


@app.get("/arkiver",
         status_code=status.HTTP_200_OK,
         response_model=List[Arkivuttrekk],
         tags=["arkivuttrekk"],
         summary="Hent alle arkivuttrekk")
def get_archives(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_all_arkivuttrekk(db, skip, limit)


