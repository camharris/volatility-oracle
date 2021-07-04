from fastapi import FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import Any, Optional
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN, HTTP_200_OK
import volatility_oracle.integrations.uniswap as uniswap
import volatility_oracle.integrations.balancer as balancer
import os


X_API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)
app = FastAPI()

def get_api_key(header: str = Security(X_API_KEY_HEADER)):
    """ Retrieves api key and validates it"""
    if header == os.getenv('API_KEY'):
        return header

    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )


class Request(BaseModel):
    id: str
    data: Any

class Response(BaseModel):
    jobRunID: str
    data: Any
    result: Optional[Any]
    statusCode: Optional[int]



@app.get('/healthcheck', response_model=Response)
def health_check():
    """
    Endpoint for manual and automated health checks
    """
    return Response(jobRunID=1, data={True})


@app.get('/uniswap_v2/pairs', response_model=Response, dependencies=[Security(get_api_key)])
def get_pairs():
    """
    Return a list of all the uniswap token pairs. 
    """
    pair_data = uniswap.get_pairs_v2()
    return Response(jobRunID=1, data=pair_data)


@app.post('/uniswap_v2/pair_apy', response_model=Response, dependencies=[Security(get_api_key)])
def get_pairs(request: Request):
    """
    Return uniswap daily pair data for time period (10/50/100 days) 
    Parameters: data {
        pool,
        range
    }
    """
    # Raise error if data is missing pool or range 
    if 'pool' not in request.data or 'range' not in request.data:
        raise HTTPException(
            status_code=400,
            detail="data must include 'pool' and 'range'"
        )


    pair_data = uniswap.get_pair_apy_v2(request.data['pool'], request.data['range'])
    return Response(
        jobRunID=request.id,
        data=pair_data,
        # if an error occurred and no apy_std is returned the result is 0
        result= 0 if 'apy_std' not in pair_data else pair_data['apy_std'],
        statusCode=200 if 'error' not in pair_data else 400
    )

@app.get('/balancer_v1/pools', response_model=Response, dependencies=[Security(get_api_key)])
def get_pools_v1():
    """
    Return a list of the top pools by volume
    """
    pools = balancer.get_top_pools_v1()
    return Response(jobRunID=1, data=pools)

@app.get('/balancer_v2/pools', response_model=Response, dependencies=[Security(get_api_key)])
def get_pools_v2():
    """
    Return a list of the top pools by volume
    """
    pools = balancer.get_top_pools_v2()
    return Response(jobRunID=1, data=pools)

@app.post('/balancer_v1/pool_apy', response_model=Response, dependencies=[Security(get_api_key)])
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
