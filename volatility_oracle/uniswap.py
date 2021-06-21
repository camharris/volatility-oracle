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
def get_pair_day_data(pair_address, range):
    client = init_client()

    daily_APYs = []
    current_time = calendar.timegm(time.gmtime())

    # Calculate epoch time of date deltas 
    time_10_days  = current_time - 864000  # 10 days in seconds
    time_50_days  = current_time - 4320000 # 50 days in seconds
    time_100_days = current_time - 8640000 # 100 days in seconds 


    if range != 10 and range != 50 and range != 100:
        return "Invalid date range: {}".format(range)
    elif range == 10:
        end_date = time_10_days
    elif range == 50:
        end_date = time_50_days
    elif range == 100:
        end_date = time_100_days


    query = gql(
    """
    query ($address: Bytes!, $enddate: Int!) {
        pairDayDatas(first: 100, orderBy: date, orderDirection: asc,
        where: {
            pairAddress: $address,
            date_gt: $enddate
    }
    ) {
        date
        dailyVolumeToken0
        dailyVolumeToken1
        dailyVolumeUSD
        totalSupply
        reserveUSD
    }
    }
    """)
    params = {
        "address": pair_address,
        "enddate": end_date,
        }

    result = client.execute(query, variable_values=params)

    client.close()

    # Calculate daily APY for each date
    # [(daily volume * fee %) / total liquidity] * 365
    for day in result['pairDayDatas']:

        fee = 1 # Not sure how to get the fee yet
        daily_APY = ((float(day['dailyVolumeUSD']) * fee) / float(day['totalSupply'])) * 365
        daily_APYs.append(daily_APY)


    # Get Average of list of the daily apy's for time period
    average_apy = sum(daily_APYs) / len(daily_APYs)


    # return result['pairDayDatas']
    return average_apy