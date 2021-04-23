#!/usr/bin/env python3
import logging
import os

from fastapi import FastAPI, status
from app.jobs.schedule_status_receiver_job import init_scheduled_job
from app.routers import arkivuttrekk, metadatafil

logging.basicConfig(level=logging.INFO, format='%(name)s | %(levelname)s | %(message)s')
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
logging.getLogger('uamqp').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass

RUN_SCHEDULER = os.getenv('RUN_SCHEDULER', 'True').lower() == 'true'


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

if os.getenv("PYTHON_ENV", None) == "local":
    from fastapi.middleware.cors import CORSMiddleware
    logger.info("Running locally")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def init_jobs():
    if RUN_SCHEDULER:
        app.scheduler = await init_scheduled_job()
        logger.info("Starting scheduler")
        app.scheduler.start()
    else:
        logger.info("Not starting scheduler")


@app.on_event("shutdown")
async def teardown_jobs():
    if RUN_SCHEDULER:
        logger.info("Shutting down scheduler")
        app.scheduler.shutdown()


if __name__ == '__main__':
    import uvicorn
    print("Starting mottak-arkiv-service")
    uvicorn.run(app, host="0.0.0.0", port=8000)
