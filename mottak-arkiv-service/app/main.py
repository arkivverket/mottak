#!/usr/bin/env python3
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import exc
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.routers import arkivuttrekk, metadatafil

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


# TODO Fix Exception handler
# Exception handlers
@app.exception_handler(exc.NoResultFound)
def sqlalchemy_exception_handler(request: Request, exception: exc.NoResultFound):
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


app.include_router(
    arkivuttrekk.router,
    prefix="/arkivuttrekk",
    tags=['arkivuttrekk'])
app.include_router(
    metadatafil.router,
    prefix="/metadatafil",
    tags=['metadatafil'])
# app.add_exception_handler(exc.NoResultFound, sqlalchemy_exception_handler)
