#!/usr/bin/env python3
import logging

from fastapi import FastAPI, status

from app.jobs.schedule_status_receiver_job import init_scheduled_job
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


# TODO Implementere helsesjekk av applikasjonen
@app.get("/health",
         status_code=status.HTTP_200_OK,
         tags=["health"],
         summary="Helsesjekk av applikasjonen")
async def health_check():
    return "Seems healthy"


app.scheduler = None
app.queue_name = None
app.include_router(
    router=arkivuttrekk.router,
    prefix="/arkivuttrekk",
    tags=['arkivuttrekk'])
app.include_router(
    router=metadatafil.router,
    prefix="/metadatafil",
    tags=['metadatafil'])


@app.on_event("startup")
async def init_jobs():
    app.scheduler, app.queue_name = await init_scheduled_job()
    logging.info(f"Starting receiving messages on queue {app.queue_name}")
    app.scheduler.start()


@app.on_event("shutdown")
async def teardown_jobs():
    logging.info(f"Closing receiver {app.queue_name}")
    app.scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn

    print("Starting mottak-arkiv-service")
    uvicorn.run(app, host="0.0.0.0", port=8000)
