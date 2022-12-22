import pandas as pd
import nasdaqdatalink as ndl
import functools as ft
from stats_can import StatsCan
import matplotlib.pyplot as plt
import os 

data_dir = os.getcwd() + "\data"

plt.close("all")


def getNASDAQData():
    ndl.save_key("GgjKAD18oK9axQgmxLsM","ndl_api")
    # ndl.read_key(filename="C:\Users\hahn\OneDrive - Wesgroup Properties\Documents - #Marketintel\Admin\Process Docs\For Harry\001 Economic Reports\data python\ndl_api")

    steel_raw = ndl.get("FRED/WPU101707")
    lumber_raw = ndl.get("FRED/WPU081")
    fr_truck_raw = ndl.get("FRED/PCU484121484121")

    steel_df = pd.DataFrame(data=steel_raw)
    # steel_df.rename(columns={'Value': 'steel price index'})
    steel_df.columns = ['steel price index']

    lumber_df = pd.DataFrame(data=lumber_raw)
    # lumber_df.rename(columns={"Value": "lumber price index"},errors="raise")
    lumber_df.columns = ['lumber price index']

    fr_truck_df = pd.DataFrame(data=fr_truck_raw)
    # fr_truck_df.rename(columns={'Value': 'freight truck price index'})
    fr_truck_df.columns = ['freight truck price index']

    # steel_df['Datevalue'] = pd.to_datetime(steel_df.index,format='%Y-%M-%D')
    # steel_df.set_index('Datevalue',append=True)
    # steel_df.drop('Date')
    # steel_df.info()

    dfs = []

    dfs.append(steel_df)
    dfs.append(lumber_df)
    dfs.append(fr_truck_df)

    comm_df = ft.reduce(lambda left, right: pd.merge(left,right,how='outer',on='Date'),dfs)
    ax = comm_df.plot(kind="line",grid=True)
    ax.text(0.5,-1, """Tracking commodity indices over time by comparing with the base year at which index = 100.\n e.g.
                            Index of 150 means the price is 50% more expensive than base year.""")
    plt.show()

    exportData(comm_df, "commodities index")

def getCANData():
    sc = StatsCan()
    dfs = []

    # inf_raw = sc.table_to_df("18-10-0259-01")
    # inf_df = pd.DataFrame(data=inf_raw)
    # print(inf_df.columns)
    # inf_df = inf_df.drop_duplicates()
    # inf_df = inf_df[~inf_df["GEO"].str.contains("Canada|British Columbia") == False]
    # keeping rows with CPI COMMON ONLY 
    # inf_df = inf_df[~inf_df["Alternative measures"].str.contains("CPI-common") == False]
    # inf_df = inf_df[['REF_DATE','GEO','Alternative measures','VALUE']]

    # dfs.append(inf_df)
    # print(inf_df)
   
    # exportData(inf_df, "inflation")

    unemp_raw = sc.table_to_df("14-10-0287-03")
    print(unemp_raw)
    unemp_df = pd.DataFrame(data=unemp_raw)
    unemp_df = unemp_df[~unemp_df["GEO"].str.contains("Canada|British Columbia") == False]
    unemp_df = unemp_df.dropna()
    dfs.append(unemp_df)
  
    exportData(unemp_df, "unemployment")

    cpi_df = ft.reduce(lambda left, right: pd.merge(left,right,how='outer',on='REF_DATE'),dfs)
    ax = cpi_df['REF_DATE','VALUEE'].plot(kind="line",grid=True)
    ax.text(0.5,-1, """Tracking inflation changes over time.""")
    plt.show()

def getCSVData():

    dfs = []
    cpi_df = pd.read_csv(os.getcwd() + '\\data\\CPI.csv')
    nhpi_df = pd.read_csv(os.getcwd() + '\\data\\New Housing Price Index.csv')


    cpi_df = cpi_df.melt('REF_DATE', var_name = 'GEO',value_name = 'CPI')
    # cpi_df['REF_DATE'] = pd.to_datetime(cpi_df.index.astype(str),format='%Y-%M-%D]')
    print(cpi_df)
    dfs.append(cpi_df)

    nhpi_df = nhpi_df.replace('Total', 'Land & House', regex=True)
    nhpi_df = nhpi_df.replace('Vancouver, British Columbia', 'Vancouver', regex=True)
    nhpi_df = nhpi_df.replace('British Columbia 6', 'British Columbia', regex=True)
    # nhpi_df['REF_DATE'] = pd.to_datetime(nhpi_df.index.astype(str),format='%Y-%M-%D')
    print(nhpi_df)
    dfs.append(nhpi_df)

    cpi_df = ft.reduce(lambda left, right: pd.merge(left,right,how='outer',on=['REF_DATE','GEO']),dfs)
    cpi_df = cpi_df[~cpi_df["GEO"].str.contains("Vancouver") == False]
    exportData(cpi_df,"inflation")
    ax = cpi_df.plot(x = 'REF_DATE',kind="line",grid=True)
    ax.text(0.5,-1, """Tracking inflation changes over time.""")
    plt.show()

def getData():
    # getNASDAQData()
    # getCANData()
    getCSVData()

def exportData(data,name):
        with pd.ExcelWriter('Economic Indicator - Cleaned.xlsx') as writer:
            data.to_excel(writer, sheet_name = name)

if __name__ == "__main__":
    getData()
    #testing commit
