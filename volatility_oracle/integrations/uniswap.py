from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import pandas as pd
import calendar
import time 


# Initialize gql client
def init_client_v2():
    endpoint='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'
    transport=RequestsHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client



def init_client_v3():
    endpoint='https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
    transport=RequestsHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client

# Get pairs
def get_pairs_v2():
    client = init_client_v2()
    # TODO sort on volume
    query = gql(
        """
        {
            pairs(first: 100, orderBy: txCount, orderDirection: desc) {
                id,
                token0 {
                id
                },
                token1 {
                id
                },
                volumeUSD,
                txCount
            }
        }
        """)

    result = client.execute(query)
    client.close()
    return result['pairs']


# Get pairDayData
def get_pair_apy_v2(pair_address, range):
    client = init_client_v2()

    daily_APYs = []
    current_time = calendar.timegm(time.gmtime())

    # Calculate epoch time of date deltas 
    time_10_days  = current_time - 864000  # 10 days in seconds
    time_50_days  = current_time - 4320000 # 50 days in seconds
    time_100_days = current_time - 8640000 # 100 days in seconds 

    # Using the chainlink client in solidity it's easier to send this as a string
    # so force this to be an int
    try:
        range = int(range)
    except:
        return { "error": "Invalid date range: {}".format(range) }

    if range != 10 and range != 50 and range != 100:
        return { "error": "Invalid date range: {}".format(range) }
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

    try:
        result = client.execute(query, variable_values=params)
    except:
        return { "error": "failed to find pool with address: {}".format(pair_address) }


    client.close()

    if len(result["pairDayDatas"]) > 1:

        # Calculate daily APY for each date
        # [(daily volume USD * fee %) / total reserves USD] * 365
        for day in result['pairDayDatas']:
            fee = 0.003 # Uniswap fee 0.3%

            try:
                daily_APY = ((float(day['dailyVolumeUSD']) * fee) / float(day['reserveUSD'])) * 365
                daily_APYs.append(daily_APY)
            except Exception as e:
                # If the above division failed it's most likely a ZeroDivisionError
                # due to daily volume and totalsupply being zero
                print(e)
                return { "apy_std": 0, "result": 0 }

        # Get Standard Deviation of the daily apy's for time period 
        try:
            daily_APYs = pd.Series(daily_APYs)
            apy_sd = daily_APYs.std()
            print(apy_sd)
            return { "apy_std": apy_sd, "result": apy_sd }
        except Exception as e:
            # If the above average fails it's because there is only one element in the list
            print(e)
            return { "apy_std": daily_APYs[0], "result": daily_APYs[0] }

    # Return zero if no historical data was found
    return { "apy_std": 0, "result": 0 }




