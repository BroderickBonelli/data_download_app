import pandas as pd
from subgrounds.subgrounds import Subgrounds
import numpy as np
import datetime as dt
from datetime import datetime
import streamlit as st
import requests
from pprint import pprint

#set pandas display format option
pd.set_option('display.float_format', lambda x: '%.2f' % x)


#protocols
lending = ['aave-v2', 'aave-v3', 'bastion-protocol', 'banker-joe', 'benqi', 'compound-v2', 'cream-finance', \
                    'iron-bank', 'maple-finance', 'moonwell']
cdps = ['abracadabra-money', 'inverse-finance', 'liquity', 'makerdao', 'qidao']

dexs = ['apeswap', 'balancer-v2', 'bancor-v3', 'beethoven-x', 'curve-finance', 'honeyswap', 'platypus-finance', 'solarbeam', 'ubeswap', 'sushiswap', 'uniswap-v3']

#lending & chain dictionary
lending_protocol_chain_dict = {
    'aave-v2':['ethereum', 'avalanche'], 'aave-v3':['optimism', 'polygon','harmony', 'fantom', 'avalanche', 'arbitrum'], \
    'bastion-protocol':['aurora'], 'banker-joe':['avalanche'], 'benqi':['avalanche'], 'compound':['ethereum'], \
    'cream-finance':['arbitrum', 'polygon', 'bsc', 'ethereum'], 'iron-bank':['fantom'], 'maple-finance':['ethereum'], \
    'moonwell':['moonriver', 'moonbeam']}

# cdp & chain dictionary
cdp_protocol_chain_dict = {
    'abracadabra-money':['ethereum', 'bsc', 'arbitrum', 'fantom', 'avalanche'], 'inverse-finance':['ethereum'], \
    'liquity':['ethereum'], 'makerdao':['ethereum'], 'qidao':['arbitrum', 'avalanche', 'bsc', 'fantom', 'polygon', 'moonriver', 'optimism', 'gnosis']
}

#DEX & chain dictionary
dex_protocol_chain_dict = {
    #'apeswap':['polygon'],
    'balancer-v2':['ethereum', 'arbitrum', 'polygon'],
    'bancor-v3':['ethereum'],
    'beethoven-x':['optimism'],
    'honeyswap':['gnosis'],
    'platypus-finance':['avalanche'],
    'solarbeam':['moonriver'],
    'ubeswap':['celo'],
    'sushiswap':['ethereum', 'celo', 'moonriver', 'moonbeam', 'avalanche', 'bsc', 'arbitrum', 'fantom', 'gnosis'],
    'uniswap-v3':['ethereum', 'polygon', 'optimism', 'arbitrum']
}

#sectors selector
sectors = {'Lending':lending_protocol_chain_dict, "CDP's":cdp_protocol_chain_dict, "DEX's":dex_protocol_chain_dict}
sector_list = [i for i in sectors]

sector = st.sidebar.selectbox(
    'Sector:',
    sector_list,
    key='sector'
)

#protocols selector
protocols = sectors[sector]
protocols_list = [i for i in protocols]

protocol = st.sidebar.selectbox(
    'Protocol:',
    protocols_list,
    key='protocol'
)

#chains selector
if sector == 'Lending':
    chains = lending_protocol_chain_dict[protocol]
elif sector == "CDP's":
    chains = cdp_protocol_chain_dict[protocol]
elif sector == "DEX's":
    chains = dex_protocol_chain_dict[protocol]

chain_list = [i for i in chains]

chain = st.sidebar.selectbox(
    'Chain:',
    chain_list,
    key='chain'
)

#get protocol & chain to obtain url for endpoint
protocol_and_chain = str(protocol) + '-' + str(chain)

url_dict = {
    'aave-v2-ethereum':'https://api.thegraph.com/subgraphs/name/messari/aave-v2-ethereum',
    'aave-v2-avalanche':'https://api.thegraph.com/subgraphs/name/messari/aave-v2-avalanche',
    'aave-v3-optimism':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-optimism-extended',
    'aave-v3-polygon':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-polygon',
    'aave-v3-harmony':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-harmony',
    'aave-v3-fantom':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-fantom',
    'aave-v3-avalanche':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-avalanche',
    'aave-v3-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/aave-v3-arbitrum',
    'bastion-protocol-aurora':'https://api.thegraph.com/subgraphs/name/messari/bastion-protocol-aurora',
    'banker-joe-avalanche':'https://api.thegraph.com/subgraphs/name/messari/banker-joe-avalanche',
    'benqi-avalanche':'https://api.thegraph.com/subgraphs/name/messari/benqi-avalanche',
    'compound-ethereum':'https://api.thegraph.com/subgraphs/name/messari/compound-ethereum',
    'cream-finance-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/cream-finance-arbitrum',
    'cream-finance-polygon':'https://api.thegraph.com/subgraphs/name/messari/cream-finance-polygon',
    'cream-finance-bsc':'https://api.thegraph.com/subgraphs/name/messari/cream-finance-bsc',
    'cream-finance-ethereum':'https://api.thegraph.com/subgraphs/name/messari/cream-finance-ethereum',
    'iron-bank-fantom':'https://api.thegraph.com/subgraphs/name/messari/iron-bank-fantom',
    'maple-finance-ethereum':'https://api.thegraph.com/subgraphs/name/messari/maple-finance-ethereum',
    'moonwell-moonriver':'https://api.thegraph.com/subgraphs/name/messari/moonwell-moonriver',
    'moonwell-moonbeam':'https://api.thegraph.com/subgraphs/name/messari/moonwell-moonbeam',
    'abracadabra-money-ethereum':'https://api.thegraph.com/subgraphs/name/messari/abracadabra-money-ethereum',
    'abracadabra-money-bsc':'https://api.thegraph.com/subgraphs/name/messari/abracadabra-money-bsc',
    'abracadabra-money-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/abracadabra-money-arbitrum',
    'abracadabra-money-fantom':'https://api.thegraph.com/subgraphs/name/messari/abracadabra-money-fantom',
    'abracadabra-money-avalanche':'https://api.thegraph.com/subgraphs/name/messari/abracadabra-money-avalanche',
    'inverse-finance-ethereum':'https://api.thegraph.com/subgraphs/name/messari/inverse-finance-ethereum',
    'liquity-ethereum':'https://api.thegraph.com/subgraphs/name/messari/liquity-ethereum',
    'makerdao-ethereum':'https://api.thegraph.com/subgraphs/name/messari/makerdao-ethereum',
    'qidao-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/qidao-arbitrum',
    'qidao-avalanche':'https://api.thegraph.com/subgraphs/name/messari/qidao-avalanche',
    'qidao-bsc':'https://api.thegraph.com/subgraphs/name/messari/qidao-bsc',
    'qidao-fantom':'https://api.thegraph.com/subgraphs/name/messari/qidao-fantom',
    'qidao-polygon':'https://api.thegraph.com/subgraphs/name/messari/qidao-polygon',
    'qidao-moonriver':'https://api.thegraph.com/subgraphs/name/messari/qidao-moonriver',
    'qidao-optimism':'https://api.thegraph.com/subgraphs/name/messari/qidao-optimism',
    'qidao-gnosis':'https://api.thegraph.com/subgraphs/name/messari/qidao-gnosis',
    'apeswap-polygon':'https://api.thegraph.com/subgraphs/name/messari/apeswap-polygon',
    'balancer-v2-ethereum':'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-ethereum',
    'balancer-v2-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-arbitrum',
    'balancer-v2-polygon':'https://api.thegraph.com/subgraphs/name/messari/balancer-v2-polygon',
    'bancor-v3-ethereum':'https://api.thegraph.com/subgraphs/name/messari/bancor-v3-ethereum',
    'beethoven-x-optimism':'https://api.thegraph.com/subgraphs/name/messari/beethoven-x-optimism',
    'honeyswap-gnosis':'https://api.thegraph.com/subgraphs/name/messari/honeyswap-gnosis',
    'platypus-finance-avalanche':'https://api.thegraph.com/subgraphs/name/messari/platypus-finance-avalanche',
    'solarbeam-moonriver':'https://api.thegraph.com/subgraphs/name/messari/solarbeam-moonriver',
    'ubeswap-celo':'https://api.thegraph.com/subgraphs/name/messari/ubeswap-celo',
    'sushiswap-ethereum':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-ethereum',
    'sushiswap-celo':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-celo',
    'sushiswap-moonriver':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-moonriver',
    'sushiswap-moonbeam':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-moonbeam',
    'sushiswap-avalanche':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-avalanche',
    'sushiswap-bsc':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-bsc',
    'sushiswap-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-arbitrum',
    'sushiswap-fantom':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-fantom',
    'sushiswap-gnosis':'https://api.thegraph.com/subgraphs/name/messari/sushiswap-gnosis',
    'uniswap-v3-ethereum':'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-ethereum',
    'uniswap-v3-polygon':'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-polygon',
    'uniswap-v3-optimism':'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-optimism',
    'uniswap-v3-arbitrum':'https://api.thegraph.com/subgraphs/name/messari/uniswap-v3-arbitrum'
}

#get url for endpoint
url = url_dict[protocol_and_chain]

#endpoint
sg = Subgrounds()
endpoint = sg.load_subgraph(url)

#function containing query for lending protocols
def get_lending_data(endpoint):
    financials_daily_data = endpoint.Query.financialsDailySnapshots(first=10000, orderBy=endpoint.FinancialsDailySnapshot.timestamp, orderDirection='desc')
    financials_df = sg.query_df([
        financials_daily_data.timestamp,
        financials_daily_data.totalValueLockedUSD,
        financials_daily_data.protocolControlledValueUSD,
        financials_daily_data.dailySupplySideRevenueUSD,
        financials_daily_data.cumulativeSupplySideRevenueUSD,
        financials_daily_data.dailyProtocolSideRevenueUSD,
        financials_daily_data.cumulativeProtocolSideRevenueUSD,
        financials_daily_data.dailyTotalRevenueUSD,
        financials_daily_data.cumulativeTotalRevenueUSD,
        financials_daily_data.totalDepositBalanceUSD,
        financials_daily_data.dailyDepositUSD,
        financials_daily_data.cumulativeDepositUSD,
        financials_daily_data.totalBorrowBalanceUSD,
        financials_daily_data.dailyBorrowUSD,
        financials_daily_data.cumulativeBorrowUSD,
        financials_daily_data.dailyLiquidateUSD,
        financials_daily_data.cumulativeLiquidateUSD,
        financials_daily_data.dailyWithdrawUSD,
        financials_daily_data.dailyRepayUSD
    ])

    financials_df['financialsDailySnapshots_timestamp'] = financials_df['financialsDailySnapshots_timestamp'].apply(datetime.fromtimestamp).dt.strftime('%Y-%m-%d')
    financials_df = financials_df.rename(columns={'financialsDailySnapshots_timestamp':'Timestamp', \
                                                'financialsDailySnapshots_protocolControlledValueUSD':'protocolControlledValueUSD', \
                                                'financialsDailySnapshots_totalValueLockedUSD':'totalValueLockedUSD', \
                                                'financialsDailySnapshots_dailySupplySideRevenueUSD':'dailySupplySideRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeSupplySideRevenueUSD':'cumulativeSupplySideRevenueUSD', \
                                                'financialsDailySnapshots_dailyProtocolSideRevenueUSD':'dailyProtocolSideRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeProtocolSideRevenueUSD':'cumulativeProtocolSideRevenueUSD', \
                                                'financialsDailySnapshots_dailyTotalRevenueUSD':'dailyTotalRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeTotalRevenueUSD':'cumulativeTotalRevenueUSD', \
                                                'financialsDailySnapshots_totalDepositBalanceUSD':'totalDepositBalanceUSD', \
                                                'financialsDailySnapshots_dailyDepositUSD':'dailyDepositUSD', \
                                                'financialsDailySnapshots_cumulativeDepositUSD':'cumulativeDepositUSD', \
                                                'financialsDailySnapshots_totalBorrowBalanceUSD':'totalBorrowBalanceUSD', \
                                                'financialsDailySnapshots_dailyBorrowUSD':'dailyBorrowUSD', \
                                                'financialsDailySnapshots_cumulativeBorrowUSD':'cumulativeBorrowUSD', \
                                                'financialsDailySnapshots_dailyLiquidateUSD':'dailyLiquidateUSD', \
                                                'financialsDailySnapshots_cumulativeLiquidateUSD':'cumulativeLiquidateUSD', \
                                                'financialsDailySnapshots_dailyWithdrawUSD':'dailyWithdrawUSD', \
                                                'financialsDailySnapshots_dailyRepayUSD':'dailyRepayUSD'
                                                })

    usage_daily_data = endpoint.Query.usageMetricsDailySnapshots(first=10000, orderBy=endpoint.UsageMetricsDailySnapshot.timestamp, orderDirection='desc')
    usage_df = sg.query_df([
        usage_daily_data.timestamp,
        usage_daily_data.dailyActiveUsers,
        usage_daily_data.cumulativeUniqueUsers,
        usage_daily_data.dailyTransactionCount,
        usage_daily_data.totalPoolCount
    ])


    usage_df['usageMetricsDailySnapshots_timestamp'] = usage_df['usageMetricsDailySnapshots_timestamp'].apply(datetime.fromtimestamp).dt.strftime('%Y-%m-%d')
    usage_df = usage_df.rename(columns={'usageMetricsDailySnapshots_timestamp':'Timestamp', \
                                        'usageMetricsDailySnapshots_dailyActiveUsers':'dailyActiveUsers', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueUsers':'cumulativeUniqueUsers', \
                                    'usageMetricsDailySnapshots_dailyActiveDepositors':'dailyActiveDepositors', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueDepositors':'cumulativeUniqueDepositors', \
                                    'usageMetricsDailySnapshots_dailyActiveBorrowers':'dailyActiveBorrowers', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueBorrowers':'cumulativeUniqueBorrowers', \
                                    'usageMetricsDailySnapshots_dailyActiveLiquidators':'dailyActiveLiquidators', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueLiquidators':'cumulativeUniqueLiquidators', \
                                    'usageMetricsDailySnapshots_dailyActiveLiquidatees':'dailyActiveLiquidatees', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueLiquidatees':'cumulativeUniqueLiquidatees', \
                                    'usageMetricsDailySnapshots_dailyTransactionCount':'dailyTransactionCount', \
                                    'usageMetricsDailySnapshots_dailyDepositCount':'dailyDepositCount', \
                                    'usageMetricsDailySnapshots_dailyWithdrawCount':'dailyWithdrawCount', \
                                    'usageMetricsDailySnapshots_dailyBorrowCount':'dailyBorrowCount', \
                                    'usageMetricsDailySnapshots_dailyRepayCount':'dailyRepayCount', \
                                    'usageMetricsDailySnapshots_dailyLiquidateCount':'dailyLiquidateCount', \
                                    'usageMetricsDailySnapshots_totalPoolCount':'totalPoolCount'})

    combined_df = pd.merge(financials_df, usage_df, on='Timestamp')
    return combined_df

#get DEX data
def get_dex_data(endpoint):
    financials_daily_data = endpoint.Query.financialsDailySnapshots(first=10000, orderBy=endpoint.FinancialsDailySnapshot.timestamp, orderDirection='desc')
    financials_df = sg.query_df([
        financials_daily_data.timestamp,
        financials_daily_data.totalValueLockedUSD,
        financials_daily_data.protocolControlledValueUSD,
        financials_daily_data.dailyVolumeUSD,
        financials_daily_data.cumulativeVolumeUSD,
        financials_daily_data.dailySupplySideRevenueUSD,
        financials_daily_data.cumulativeSupplySideRevenueUSD,
        financials_daily_data.dailyProtocolSideRevenueUSD,
        financials_daily_data.cumulativeProtocolSideRevenueUSD,
        financials_daily_data.dailyTotalRevenueUSD,
        financials_daily_data.cumulativeTotalRevenueUSD
    ])


    financials_df['financialsDailySnapshots_timestamp'] = financials_df['financialsDailySnapshots_timestamp'].apply(datetime.fromtimestamp).dt.strftime('%Y-%m-%d')
    financials_df = financials_df.rename(columns={'financialsDailySnapshots_timestamp':'Timestamp', \
                                                'financialsDailySnapshots_protocolControlledValueUSD':'protocolControlledValueUSD', \
                                                'financialsDailySnapshots_totalValueLockedUSD':'totalValueLockedUSD', \
                                                'financialsDailySnapshots_dailyVolumeUSD':'dailyVolumeUSD', \
                                                'financialsDailySnapshots_cumulativeVolumeUSD':'cumulativeVolumeUSD', \
                                                'financialsDailySnapshots_dailySupplySideRevenueUSD':'dailySupplySideRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeSupplySideRevenueUSD':'cumulativeSupplySideRevenueUSD', \
                                                'financialsDailySnapshots_dailyProtocolSideRevenueUSD':'dailyProtocolSideRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeProtocolSideRevenueUSD':'cumulativeProtocolSideRevenueUSD', \
                                                'financialsDailySnapshots_dailyTotalRevenueUSD':'dailyTotalRevenueUSD', \
                                                'financialsDailySnapshots_cumulativeTotalRevenueUSD':'cumulativeTotalRevenueUSD'
                                                })

    usage_daily_data = endpoint.Query.usageMetricsDailySnapshots(first=10000, orderBy=endpoint.UsageMetricsDailySnapshot.timestamp, orderDirection='desc')
    usage_df = sg.query_df([
        usage_daily_data.timestamp,
        usage_daily_data.dailyActiveUsers,
        usage_daily_data.cumulativeUniqueUsers,
        usage_daily_data.dailyTransactionCount,
        usage_daily_data.dailySwapCount,
        usage_daily_data.totalPoolCount
    ])


    usage_df['usageMetricsDailySnapshots_timestamp'] = usage_df['usageMetricsDailySnapshots_timestamp'].apply(datetime.fromtimestamp).dt.strftime('%Y-%m-%d')
    usage_df = usage_df.rename(columns={'usageMetricsDailySnapshots_timestamp':'Timestamp', \
                                        'usageMetricsDailySnapshots_dailyActiveUsers':'dailyActiveUsers', \
                                    'usageMetricsDailySnapshots_cumulativeUniqueUsers':'cumulativeUniqueUsers', \
                                    'usageMetricsDailySnapshots_dailyTransactionCount':'dailyTransactionCount', \
                                    'usageMetricsDailySnapshots_dailySwapCount':'dailySwapCount', \
                                    'usageMetricsDailySnapshots_totalPoolCount':'totalPoolCount'})

    combined_df = pd.merge(financials_df, usage_df, on='Timestamp')
    return combined_df



st.title('Data Download Tool')
st.write('Select a sector, protocol, and chain to download data on revenues, TVL, user metrics, etc.')

#function to convert df to csv
def convert_df(df):
   return df.to_csv().encode('utf-8')

#return correct df based on sector selection
if sector == 'Lending' or sector == "CDP's":
    df = get_lending_data(endpoint)
    st.write(df)

elif sector == "DEX's":
    df = get_dex_data(endpoint)
    st.write(df)

#call convert_df function on df
csv = convert_df(df)

#download csv button
st.download_button(
   "Download CSV",
   csv,
   protocol_and_chain + ".csv",
   key='download-csv'
)