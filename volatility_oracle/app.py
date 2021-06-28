from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Optional
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import volatility_oracle.integrations.uniswap as uniswap
import volatility_oracle.integrations.balancer as balancer

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


@app.get('/uniswap_v2/pairs', response_model=Response)
def get_pairs():
    """
    Return a list of all the uniswap token pairs. 
    """
    pair_data = uniswap.get_pairs_v2()
    return Response(jobRunID=1, data=pair_data)


@app.post('/uniswap_v2/pair_apy', response_model=Response)
def get_pairs(request: Request):
    """
    Return uniswap daily pair data for time period (10/50/100 days) 
    Parameters: data {
        address,
        range
    }
    """
    # Raise error if data is missing address or range 
    if 'address' not in request.data or 'range' not in request.data:
        raise HTTPException(
            status_code=400,
            detail="data must include 'address' and 'range'"
        )


    pair_data = uniswap.get_pair_apy_v2(request.data['address'], request.data['range'])
    return Response(jobRunID=1, data=pair_data)

@app.get('/balancer_v1/pools', response_model=Response)
def get_pools_v1():
    """
    Return a list of the top pools by volume
    """
    pools = balancer.get_top_pools_v1()
    return Response(jobRunID=1, data=pools)

@app.get('/balancer_v2/pools', response_model=Response)
def get_pools_v2():
    """
    Return a list of the top pools by volume
    """
    pools = balancer.get_top_pools_v2()
    return Response(jobRunID=1, data=pools)

@app.post('/balancer_v1/pool_apy', response_model=Response)
def get_balancer_apy_v1(request: Request):
    """
    Return balancer v1 pool apy 
    Parameters: data {
        address
    }
    """
    if 'address' not in request.data:
        raise HTTPException(
            status_code=400,
            detail="data must include 'address'"
        )

    data = balancer.get_pool_apy_v1(request.data['address'])
    return Response(jobRunID=1, data=data)
