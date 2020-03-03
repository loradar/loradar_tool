#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import glob, matplotlib, pprint, requests, math, seaborn
import pandas as pd
import numpy as np
from collections import Counter
from itertools import repeat
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

dat = pd.read_csv() ## Please select the path to your data here



def DeviceList(data, network=None, frequencyplan=None, manufacturer=None):
    
    # This lists identified devices
    # Optional filters are 'network', 'frequencyplan', 'manufacturer'
    
    arg_list = [network, frequencyplan, manufacturer]
    
    # Applying the filters
    for i in range(len(arg_list)):
        if i == 0:
            if network != None:
                nwk = network
            else:
                nwk = data["network"]
        elif i == 1:
            if frequencyplan != None:
                freqplan = frequencyplan
            else:
                freqplan = data["Freq_Plan"]
        elif i == 2:
            if manufacturer != None:
                manf = manufacturer
            else:
                manf = data["deveui_manufacturer"]

    # Output the result
    result = data.loc[(data["Freq_Plan"] == freqplan) &
                      (data["network"] == nwk) &
                      (data["deveui_manufacturer"] == manf)]
    result = result[["DevEUI or DevAddr", "Freq_Plan",
                     "network", "deveui_manufacturer"]]
    return(result.to_json(orient='records'))



def ChannelOccupancy(data, datarate=None, frequencyplan=None):
    
    # This lists channel-wise packet distribution
    # Optional filters can be 'datarate' and 'frequencyplan'
    
    arg_list = [datarate, frequencyplan]
    
    for i in range(len(arg_list)):
        if i == 0:
            if datarate != None:
                dr = datarate
            else:
                dr = data["datarate"]
        elif i == 1:
            if frequencyplan != None:
                freqplan = frequencyplan
            else:
                freqplan = data["Freq_Plan"]

    # Applying the filters
    filt = data.loc[(data["datarate"] == dr) & (data["Freq_Plan"] == freqplan)]
    
    # Cleaning the data format
    filt = list(zip(filt["datarate"].str.strip(), filt["frequency"]/1000000))

    # Counting packets
    count = Counter(filt)
    df = pd.DataFrame(count.values(),
                      index=pd.MultiIndex.from_tuples(count.keys())).unstack(1)
    result = df.fillna(0)[0].sort_index(axis=0)

    # Converting to percentage
    result = result.div(result.values.sum()/100)

    return(result.round(2).to_json(orient='columns'))



def RSSI(data, network=None, frequencyplan=None, manufacturer=None):
    
    # This shows the distribution of RSSI in percentage
    # Optional filters are 'network', 'frequencyplan', 'manufacturer'
    
    arg_list = [network, frequencyplan, manufacturer]
    
    # Applying the filters
    for i in range(len(arg_list)):
        if i == 0:
            if network != None:
                nwk = network
            else:
                nwk = data["network"]
        elif i == 1:
            if frequencyplan != None:
                freqplan = frequencyplan
            else:
                freqplan = data["Freq_Plan"]
        elif i == 2:
            if manufacturer != None:
                manf = manufacturer
            else:
                manf = data["deveui_manufacturer"]

    # Output the result
    result = data.loc[(data["Freq_Plan"] == freqplan) &
                      (data["network"] == nwk) &
                      (data["deveui_manufacturer"] == manf)]
    
    # Create a new dataframe of the RSSI
    rssi_data = zip(Counter(result["RSSI"]).keys(), Counter(result["RSSI"]).values())
    result = pd.DataFrame(rssi_data, columns = ["RSSI", "Percentage"])
    
    # Converting to percentage
    result["Percentage"] = np.round((result["Percentage"]/result["Percentage"].sum())*100, 3)
    
    #return(result)
    return(result.to_json(orient='records'))



def SNR(data, network=None, frequencyplan=None, manufacturer=None):
    
    # This shows the distribution of RSSI in percentage
    # Optional filters are 'network', 'frequencyplan', 'manufacturer'
    
    arg_list = [network, frequencyplan, manufacturer]
    
    # Applying the filters
    for i in range(len(arg_list)):
        if i == 0:
            if network != None:
                nwk = network
            else:
                nwk = data["network"]
        elif i == 1:
            if frequencyplan != None:
                freqplan = frequencyplan
            else:
                freqplan = data["Freq_Plan"]
        elif i == 2:
            if manufacturer != None:
                manf = manufacturer
            else:
                manf = data["deveui_manufacturer"]

    # Output the result
    result = data.loc[(data["Freq_Plan"] == freqplan) &
                      (data["network"] == nwk) &
                      (data["deveui_manufacturer"] == manf)]
    
    # Create a new dataframe of the RSSI
    snr_data = zip(Counter(result["SNR"]).keys(), Counter(result["SNR"]).values())
    result = pd.DataFrame(snr_data, columns = ["SNR", "Percentage"])
    
    # Converting to percentage
    result["Percentage"] = np.round((result["Percentage"]/result["Percentage"].sum())*100, 3)
    
    #return(result)
    return(result.to_json(orient='records'))



def NetworkList(data, frequencyplan=None, manufacturer=None):
    
    # This lists identified devices
    # Optional filters are 'frequencyplan', 'manufacturer'
    
    arg_list = [frequencyplan, manufacturer]
    
    # Applying the filters
    for i in range(len(arg_list)):
        if i == 0:
            if frequencyplan != None:
                freqplan = frequencyplan
            else:
                freqplan = data["Freq_Plan"]
        elif i == 1:
            if manufacturer != None:
                manf = manufacturer
            else:
                manf = data["deveui_manufacturer"]
    
    result = data.loc[(data["Freq_Plan"] == freqplan) &
                      (data["deveui_manufacturer"] == manf)]
    
    # Split it from the original dataframe by DevAddr or DevEUI
    # Output the result
    l_freq = []
    freq_p = list(set(result["Freq_Plan"]))
    if len(freq_p) > 1:
        for a, b in result.groupby("Freq_Plan", sort=False):
            l_freq.append(b.sort_values(by=["sec_diff"]))
        for i in range(len(l_freq)):
            print(freq_p[i])
            result = l_freq[i].groupby("network").nunique()["DevEUI or DevAddr"]
            print(result.to_json(orient='columns'))
    
    else:
        print(freq_p[0])
        result = l_freq[0].groupby("network").nunique()["DevEUI or DevAddr"]
        print(result.to_json(orient='columns'))

