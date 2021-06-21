from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from volatility_oracle import uniswap
import json

app = FastAPI()

class Request(BaseModel):
    id: int
    data: Any

class Response(BaseModel):
    jobRunID: int
    data: Any


@app.get('/healthcheck', response_model=Response)
def health_check():
    """
    Endpoint for manual and automated health checks
    """
    return Response(jobRunID=1, data={True})


@app.get('/uniswap/getpairs', response_model=Response)
def get_pairs():
    """
    Return a list of all the uniswap token pairs 
    """
    pair_data = uniswap.get_pairs()
    return Response(jobRunID=1, data=pair_data)


@app.post('/uniswap/getpairsdata', response_model=Response)
def get_pairs(request: Request):
    """
    Return uniswap daily pair data for time period (10/50/100 days) 
    """
    # Raise error if data is missing address or range 
    

    pair_data = uniswap.get_pair_day_data(request.data['address'], request.data['range'])
    return Response(jobRunID=1, data=pair_data)