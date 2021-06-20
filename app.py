from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import Any, Optional
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

app = FastAPI()

class Request(BaseModel):
    id: int
    data: Any

class Response(BaseModel):
    jobRunID: int
    data: Any


@app.get('/healthcheck', response_model=Response)
def health_check(response=Response):
    return Response(jobRunID=1, data={True})