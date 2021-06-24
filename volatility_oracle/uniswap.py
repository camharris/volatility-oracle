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

    if len(result["pairDayDatas"]) > 1:

        # Calculate daily APY for each date
        # [(daily volume * fee %) / total liquidity] * 365
        for day in result['pairDayDatas']:
            fee = 0.003 # Uniswap fee 0.3%

            try:
                daily_APY = ((float(day['dailyVolumeUSD']) * fee) // float(day['totalSupply'])) * 365
                daily_APYs.append(daily_APY)
            except:
                # If the above division failed it's most likely a ZeroDivisionError
                # due to daily volume and totalsupply being zero
                return 0


        # Get Average of list of the daily apy's for time period 
        try:
            average_apy = sum(daily_APYs) // len(daily_APYs)
            return average_apy
        except:
            # If the above average fails it's because there is only one element in the list
            return daily_APYs[0]

    # Return zero if no historical data was found
    return 0

    def calc_imperm_loss():

        return True