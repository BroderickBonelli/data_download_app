import pandas as pd
from subgrounds.subgrounds import Subgrounds
import numpy as np
import datetime as dt
from datetime import datetime
import streamlit as st
import requests

# set pandas display format option
pd.set_option("display.float_format", lambda x: "%.2f" % x)


url = "https://subgraphs.messari.io/deployments.json"
response = requests.get(url).json()
exchanges = response["exchanges"]
lenders = response["lending"]
vaults = response["vaults"]
liquid_staking = response["generic"]


# sectors selector
sectors = ["Lending", "DEXs", "Yield Aggregators"]

sector = st.sidebar.selectbox("Sector:", sectors)

# protocols selector
if sector == "DEXs":
    deployments = response["exchanges"]
    protocols = list(deployments.keys())
    protocols.remove("apeswap")  # times out
    protocols.remove("spiritswap")  # times out
    protocols.remove("spookyswap")  # times out
    protocols.remove("curve")  # old schema
    protocols.remove("ellipsis-finance")  # old schema
elif sector == "Lending":
    deployments = response["lending"]
    protocols = list(deployments.keys())
    protocols.remove("makerdao")
elif sector == "Yield Aggregators":
    deployments = response["vaults"]
    protocols = list(deployments.keys())
# elif sector == "Generic":
#     deployments = response["generic"]
#     protocols = list(deployments.keys())

protocol = st.sidebar.selectbox("Protocol:", protocols)

protocol_chains = list(deployments[protocol].keys())
chain = st.sidebar.selectbox("Chains: ", protocol_chains)

# get url for endpoint
url = deployments[protocol][chain]

# endpoint
sg = Subgrounds()
endpoint = sg.load_subgraph(url)


################################################################################
# Query Functions

# function containing query for lending protocols
def get_lending_data(endpoint):
    financials_daily_data = endpoint.Query.financialsDailySnapshots(
        first=10000,
        orderBy=endpoint.FinancialsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    financials_df = sg.query_df(
        [
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
            financials_daily_data.dailyRepayUSD,
        ]
    )

    financials_df["financialsDailySnapshots_timestamp"] = (
        financials_df["financialsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    financials_df = financials_df.rename(
        columns={
            "financialsDailySnapshots_timestamp": "Timestamp",
            "financialsDailySnapshots_protocolControlledValueUSD": "protocolControlledValueUSD",
            "financialsDailySnapshots_totalValueLockedUSD": "totalValueLockedUSD",
            "financialsDailySnapshots_dailySupplySideRevenueUSD": "dailySupplySideRevenueUSD",
            "financialsDailySnapshots_cumulativeSupplySideRevenueUSD": "cumulativeSupplySideRevenueUSD",
            "financialsDailySnapshots_dailyProtocolSideRevenueUSD": "dailyProtocolSideRevenueUSD",
            "financialsDailySnapshots_cumulativeProtocolSideRevenueUSD": "cumulativeProtocolSideRevenueUSD",
            "financialsDailySnapshots_dailyTotalRevenueUSD": "dailyTotalRevenueUSD",
            "financialsDailySnapshots_cumulativeTotalRevenueUSD": "cumulativeTotalRevenueUSD",
            "financialsDailySnapshots_totalDepositBalanceUSD": "totalDepositBalanceUSD",
            "financialsDailySnapshots_dailyDepositUSD": "dailyDepositUSD",
            "financialsDailySnapshots_cumulativeDepositUSD": "cumulativeDepositUSD",
            "financialsDailySnapshots_totalBorrowBalanceUSD": "totalBorrowBalanceUSD",
            "financialsDailySnapshots_dailyBorrowUSD": "dailyBorrowUSD",
            "financialsDailySnapshots_cumulativeBorrowUSD": "cumulativeBorrowUSD",
            "financialsDailySnapshots_dailyLiquidateUSD": "dailyLiquidateUSD",
            "financialsDailySnapshots_cumulativeLiquidateUSD": "cumulativeLiquidateUSD",
            "financialsDailySnapshots_dailyWithdrawUSD": "dailyWithdrawUSD",
            "financialsDailySnapshots_dailyRepayUSD": "dailyRepayUSD",
        }
    )

    usage_daily_data = endpoint.Query.usageMetricsDailySnapshots(
        first=10000,
        orderBy=endpoint.UsageMetricsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    usage_df = sg.query_df(
        [
            usage_daily_data.timestamp,
            usage_daily_data.dailyActiveUsers,
            usage_daily_data.cumulativeUniqueUsers,
            usage_daily_data.dailyTransactionCount,
            usage_daily_data.totalPoolCount,
        ]
    )

    usage_df["usageMetricsDailySnapshots_timestamp"] = (
        usage_df["usageMetricsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    usage_df = usage_df.rename(
        columns={
            "usageMetricsDailySnapshots_timestamp": "Timestamp",
            "usageMetricsDailySnapshots_dailyActiveUsers": "dailyActiveUsers",
            "usageMetricsDailySnapshots_cumulativeUniqueUsers": "cumulativeUniqueUsers",
            "usageMetricsDailySnapshots_dailyActiveDepositors": "dailyActiveDepositors",
            "usageMetricsDailySnapshots_cumulativeUniqueDepositors": "cumulativeUniqueDepositors",
            "usageMetricsDailySnapshots_dailyActiveBorrowers": "dailyActiveBorrowers",
            "usageMetricsDailySnapshots_cumulativeUniqueBorrowers": "cumulativeUniqueBorrowers",
            "usageMetricsDailySnapshots_dailyActiveLiquidators": "dailyActiveLiquidators",
            "usageMetricsDailySnapshots_cumulativeUniqueLiquidators": "cumulativeUniqueLiquidators",
            "usageMetricsDailySnapshots_dailyActiveLiquidatees": "dailyActiveLiquidatees",
            "usageMetricsDailySnapshots_cumulativeUniqueLiquidatees": "cumulativeUniqueLiquidatees",
            "usageMetricsDailySnapshots_dailyTransactionCount": "dailyTransactionCount",
            "usageMetricsDailySnapshots_dailyDepositCount": "dailyDepositCount",
            "usageMetricsDailySnapshots_dailyWithdrawCount": "dailyWithdrawCount",
            "usageMetricsDailySnapshots_dailyBorrowCount": "dailyBorrowCount",
            "usageMetricsDailySnapshots_dailyRepayCount": "dailyRepayCount",
            "usageMetricsDailySnapshots_dailyLiquidateCount": "dailyLiquidateCount",
            "usageMetricsDailySnapshots_totalPoolCount": "totalPoolCount",
        }
    )

    combined_df = pd.merge(financials_df, usage_df, on="Timestamp")
    return combined_df


# get DEX data
def get_dex_data(endpoint):
    financials_daily_data = endpoint.Query.financialsDailySnapshots(
        first=10000,
        orderBy=endpoint.FinancialsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    financials_df = sg.query_df(
        [
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
            financials_daily_data.cumulativeTotalRevenueUSD,
        ]
    )

    financials_df["financialsDailySnapshots_timestamp"] = (
        financials_df["financialsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    financials_df = financials_df.rename(
        columns={
            "financialsDailySnapshots_timestamp": "Timestamp",
            "financialsDailySnapshots_protocolControlledValueUSD": "protocolControlledValueUSD",
            "financialsDailySnapshots_totalValueLockedUSD": "totalValueLockedUSD",
            "financialsDailySnapshots_dailyVolumeUSD": "dailyVolumeUSD",
            "financialsDailySnapshots_cumulativeVolumeUSD": "cumulativeVolumeUSD",
            "financialsDailySnapshots_dailySupplySideRevenueUSD": "dailySupplySideRevenueUSD",
            "financialsDailySnapshots_cumulativeSupplySideRevenueUSD": "cumulativeSupplySideRevenueUSD",
            "financialsDailySnapshots_dailyProtocolSideRevenueUSD": "dailyProtocolSideRevenueUSD",
            "financialsDailySnapshots_cumulativeProtocolSideRevenueUSD": "cumulativeProtocolSideRevenueUSD",
            "financialsDailySnapshots_dailyTotalRevenueUSD": "dailyTotalRevenueUSD",
            "financialsDailySnapshots_cumulativeTotalRevenueUSD": "cumulativeTotalRevenueUSD",
        }
    )

    usage_daily_data = endpoint.Query.usageMetricsDailySnapshots(
        first=10000,
        orderBy=endpoint.UsageMetricsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    usage_df = sg.query_df(
        [
            usage_daily_data.timestamp,
            usage_daily_data.dailyActiveUsers,
            usage_daily_data.cumulativeUniqueUsers,
            usage_daily_data.dailyTransactionCount,
            usage_daily_data.dailySwapCount,
            usage_daily_data.totalPoolCount,
        ]
    )

    usage_df["usageMetricsDailySnapshots_timestamp"] = (
        usage_df["usageMetricsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    usage_df = usage_df.rename(
        columns={
            "usageMetricsDailySnapshots_timestamp": "Timestamp",
            "usageMetricsDailySnapshots_dailyActiveUsers": "dailyActiveUsers",
            "usageMetricsDailySnapshots_cumulativeUniqueUsers": "cumulativeUniqueUsers",
            "usageMetricsDailySnapshots_dailyTransactionCount": "dailyTransactionCount",
            "usageMetricsDailySnapshots_dailySwapCount": "dailySwapCount",
            "usageMetricsDailySnapshots_totalPoolCount": "totalPoolCount",
        }
    )

    combined_df = pd.merge(financials_df, usage_df, on="Timestamp")
    return combined_df


def get_yield_aggregators_data(endpoint):
    financials_daily_data = endpoint.Query.financialsDailySnapshots(
        first=10000,
        orderBy=endpoint.FinancialsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    financials_df = sg.query_df(
        [
            financials_daily_data.timestamp,
            financials_daily_data.totalValueLockedUSD,
            financials_daily_data.protocolControlledValueUSD,
            financials_daily_data.dailySupplySideRevenueUSD,
            financials_daily_data.cumulativeSupplySideRevenueUSD,
            financials_daily_data.dailyProtocolSideRevenueUSD,
            financials_daily_data.cumulativeProtocolSideRevenueUSD,
            financials_daily_data.dailyTotalRevenueUSD,
            financials_daily_data.cumulativeTotalRevenueUSD,
        ]
    )

    financials_df["financialsDailySnapshots_timestamp"] = (
        financials_df["financialsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    financials_df = financials_df.rename(
        columns={
            "financialsDailySnapshots_timestamp": "Timestamp",
            "financialsDailySnapshots_protocolControlledValueUSD": "protocolControlledValueUSD",
            "financialsDailySnapshots_totalValueLockedUSD": "totalValueLockedUSD",
            "financialsDailySnapshots_dailySupplySideRevenueUSD": "dailySupplySideRevenueUSD",
            "financialsDailySnapshots_cumulativeSupplySideRevenueUSD": "cumulativeSupplySideRevenueUSD",
            "financialsDailySnapshots_dailyProtocolSideRevenueUSD": "dailyProtocolSideRevenueUSD",
            "financialsDailySnapshots_cumulativeProtocolSideRevenueUSD": "cumulativeProtocolSideRevenueUSD",
            "financialsDailySnapshots_dailyTotalRevenueUSD": "dailyTotalRevenueUSD",
            "financialsDailySnapshots_cumulativeTotalRevenueUSD": "cumulativeTotalRevenueUSD",
        }
    )

    usage_daily_data = endpoint.Query.usageMetricsDailySnapshots(
        first=10000,
        orderBy=endpoint.UsageMetricsDailySnapshot.timestamp,
        orderDirection="desc",
    )
    usage_df = sg.query_df(
        [
            usage_daily_data.timestamp,
            usage_daily_data.dailyActiveUsers,
            usage_daily_data.cumulativeUniqueUsers,
            usage_daily_data.dailyTransactionCount
            # usage_daily_data.totalPoolCount
        ]
    )

    usage_df["usageMetricsDailySnapshots_timestamp"] = (
        usage_df["usageMetricsDailySnapshots_timestamp"]
        .apply(datetime.fromtimestamp)
        .dt.strftime("%Y-%m-%d")
    )
    usage_df = usage_df.rename(
        columns={
            "usageMetricsDailySnapshots_timestamp": "Timestamp",
            "usageMetricsDailySnapshots_dailyActiveUsers": "dailyActiveUsers",
            "usageMetricsDailySnapshots_cumulativeUniqueUsers": "cumulativeUniqueUsers",
            "usageMetricsDailySnapshots_dailyTransactionCount": "dailyTransactionCount"
            #'usageMetricsDailySnapshots_totalPoolCount':'totalPoolCount'
        }
    )

    combined_df = pd.merge(financials_df, usage_df, on="Timestamp")
    return combined_df


################################################################################

st.title("Subgraph Data Download Tool")

st.write(
    "Select a sector, protocol, and chain to download subgraph data on revenues, TVL, user metrics, etc."
)

st.write("---")

st.markdown(
    "### **Note: Please check the QA status of the selected subgraph [here](https://subgraphs.messari.io) before downloading.**"
)

st.write(" ")

# function to convert df to csv
def convert_df(df):
    return df.to_csv().encode("utf-8")


# return correct df based on sector selection
if sector == "Lending":
    with st.spinner("Retrieving data from subgraph, could take up to a minute."):
        df = get_lending_data(endpoint)
        st.write(df)

elif sector == "DEXs":
    with st.spinner("Retrieving data from subgraph, could take up to a minute."):
        df = get_dex_data(endpoint)
        st.write(df)

elif sector == "Yield Aggregators":
    with st.spinner("Retrieving data from subgraph, could take up to a minute."):
        df = get_yield_aggregators_data(endpoint)
        st.write(df)

# call convert_df function on df
csv = convert_df(df)

# download csv button
st.download_button(
    "Download CSV", csv, protocol + "-" + chain + ".csv", key="download-csv"
)
