from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import calendar
import time 


# Initialize gql client
def init_client():
    endpoint='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
    transport=RequestsHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client

# Get pairs
def get_pairs():
    client = init_client()
    query = gql(
        """
        {
            pairs {
                id,
                token0 {
                id
                },
                token1 {
                id
                }
            }
        }
        """)

    result = client.execute(query)
    client.close()
    return result['pairs']


# Get pairDayData
def get_pair_day_data(pair_address, start_date, end_date):
    client = init_client()
    current_time = calendar.timegm(time.gmtime())


    query = gql(
    """    
    {
    pairDayDatas(first: 100, orderBy: date, orderDirection: asc,
    where: {
        pairAddress: "{}",
        date_gt: {}
        date_lt: {}
    }
    ) {
        date
        dailyVolumeToken0
        dailyVolumeToken1
        dailyVolumeUSD
        reserveUSD
    }
    }
    """.format(pair_address, start_date, end_date))

    result = client.execute(query)
    client.close()
    return result['pairDayDatas']