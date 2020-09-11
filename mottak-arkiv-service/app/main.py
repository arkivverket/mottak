#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hej fra ": "Arkivverket"}


@app.get("/health")
async def health_check():
    return True, "Seems healthy"



