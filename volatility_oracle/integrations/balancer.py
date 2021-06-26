from fastapi import params
from fastapi.params import Query
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import calendar 
import time

# Initialize gql client
def init_client_v1():
    endpoint='https://api.thegraph.com/subgraphs/name/balancer-labs/balancer'
    transport=RequestsHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client


def init_client_v2():
    endpoint='https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2'
    transport=RequestsHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client

# Get top pools
def get_top_pools_v1():
    client = init_client_v1()

    query = gql(
        """
        {
            pools(first: 1000, where: {publicSwap: true}) {
                id
                publicSwap
                swapFee
                tokens {
                id
                address
                balance
                decimals
                symbol
                }
            }
        }
        """)

    result = client.execute(query)
    client.close()

    return result["pools"]


def get_top_pools_v2():
    client = init_client_v2()

    query = gql(
        """
        {
            pools(first: 1000) {
                id
                swapFee
                tokens {
                id
                address
                balance
                decimals
                symbol
                }
            }
        }
        """
    )
    result = client.execute(query)
    client.close( )
    return result["pools"]

def get_pool_apy_v1(pool_address):
    client = init_client_v1()


    query = gql(
        """
        query ($pool_address: ID!) {
         pools(
             where: {
                 id: $pool_address
             }
         ) {
             id,
             symbol,
             name,
             swapFee,
             tokensList,
             tokens {
                 balance,
                 symbol,
                 decimals
             }
         }  
        }
        """
    )
    params = {
        "pool_address": pool_address
    }
    result = client.execute(query, variable_values=params)

    # TODO calculate APY


    return result["pools"]