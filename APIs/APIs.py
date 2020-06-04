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

csv_dic = {}
csv_dic[0] = "ALL csv"
docs = glob.glob("*LoRadar_data.csv")

## Calling the session
for num, name in enumerate(docs):
    csv_dic[num+1] = name

df = pd.DataFrame(csv_dic.items(), columns = ["Session Number", "Session Name"])
print(df)

dat_idx = int(input("\nPlease select the Session Number to be used: "))
print("\n")

if dat_idx == 0:
    all_dat = []
    for doc in docs:
        all_dat.append(pd.read_csv(doc, encoding = 'unicode_escape', dtype='unicode'))
        data = pd.concat(all_dat)
        data.reset_index(inplace=True)
        data = data.dropna(subset=["UTC timestamp"])
        data = data.drop("index", axis=1)
else:
    dat_input = docs[dat_idx - 1]
    data = pd.read_csv(dat_input, encoding = 'unicode_escape', dtype='unicode')
    

## Calling the APIs
api_dic = {}
api_dic[0] = "DeviceList"
api_dic[1] = "ChannelOccupancy"
api_dic[2] = "RSSI"
api_dic[3] = "SNR"
api_dic[4] = "NetworkList"
api_dic[5] = "SpectrumPolicing"
df = pd.DataFrame(api_dic.items(), columns = ["API Number", "API Name"])

print(df)
print("\n")

api_idx = int(input("\nPlease select the API Number to be used: "))
print("\n")

## Network filter
netw_l = list(set(data.loc[data.activation == "ABP"].network))
for num, netw in enumerate(netw_l):
    print(num+1,netw)
netw_idx = int(input("\nPlease specify the number corresponding to the desired network (To consider all, enter '0'): "))
print("\n")
if num == 0:
    network = None
else:
    network = netw_l[netw_idx-1]

## Frequency plan filter
frqb_l = list(set(data.Freq_Plan))
for num, frqb in enumerate(frqb_l):
    print(num+1,frqb)
frqb_idx = int(input("\nPlease specify the number corresponding to the desired frequency band (To consider all, enter '0'): "))
print("\n")
if num == 0:
    frequencyplan = None
else:
    frequencyplan = frqb_l[frqb_idx-1]

## Manufacturer filter
manu_l = list(set(data.loc[data.activation=="OTAA"].deveui_manufacturer))
for num, manu in enumerate(manu_l):
    print(num+1,manu)
manu_idx = int(input("\nPlease specify the number corresponding to the desired manufacturer (To consider all, enter '0'): "))
print("\n")
if num == 0:
    manufacturer = None
else:
    manufacturer = manu_l[manu_idx-1]


## List of APIs
def DeviceList(data=data, network=None, frequencyplan=None, manufacturer=None):
    
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



def ChannelOccupancy(data=data, datarate=None, frequencyplan=None):
    
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
    filt = list(zip(filt["datarate"].str.strip(), filt["frequency"].astype(float)/1000000))

    # Counting packets
    count = Counter(filt)
    df = pd.DataFrame(count.values(),
                      index=pd.MultiIndex.from_tuples(count.keys())).unstack(1)
    result = df.fillna(0)[0].sort_index(axis=0)

    # Converting to percentage
    result = result.div(result.values.sum()/100)

    return(result.round(2).to_json(orient='columns'))



def RSSI(data=data, network=None, frequencyplan=None, manufacturer=None):
    
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



def SNR(data=data, network=None, frequencyplan=None, manufacturer=None):
    
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



def NetworkList(data=data, frequencyplan=None, manufacturer=None):
    
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

def SpectrumPolicing(data=data):
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.edgecolor'] = 'black'
    plt.rcParams['grid.alpha'] = .9
    plt.rcParams['grid.color'] = "black"
    matplotlib.rcParams['axes.linewidth'] = 3
    plt.rc('grid', linestyle=":")
    seaborn.set_context("poster", font_scale=2, rc={"lines.linewidth": 3})

    fig, ax = plt.subplots()
    fig.set_size_inches(40, 40)

    #AS923
    size = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    sf7_250 = [23.17, 30.85, 35.97, 43.65, 51.33, 59.01, 66.69, 74.37, 82.05, 87.17, 94.85]
    sf7 = [46.34, 61.7, 71.94, 87.3, 102.66, 118.02, 133.38, 148.74, 164.1, 174.34, 189.7]
    sf8 = [82.43, 113.15, 133.63, 164.35, 184.84, 215.55, 236.03, 266.75, 287.23, 317.95, 338.43]
    sf9 = [164.86, 205.82, 246.78, 287.74, 328.7, 390.14, 431.1, 472.06, 513.02, 574.46, 615.42]
    sf10 = [288.77, 370.69, 452.61, 534.53, 616.45, 698.37, 780.29, 862.21, 944.13, 1026.05, 1107.97]
    sf11 = [577.54, 823.3, 987.14, 1150.98, 1314.82, 1478.66, 1724.42, 1888.26, 2052.1, 2215.94, 2461.7]
    sf12 = [1155.07, 1482.75, 1810.43, 2138.11, 2465.79, 2793.47, 3121.15, 3448.83, 3776.51, 4104.19, 4431.87]

    #AU915 has no 250 and sf11 & 12

    all_sf = [sf7_250, sf7, sf8, sf9, sf10, sf11, sf12]
    tx_sf = []
    times24h = (24*60*60)/(30*1000)

    for i in all_sf:
        fixed = [times24h*x for x in i]
        tx_sf.append(fixed)

    all_sf = np.column_stack(tx_sf)

    idx = ["SF7 (250kHz)", "SF7 (125kHz)", "SF8 (125kHz)", "SF9 (125kHz)", "SF10 (125kHz)", "SF11 (125kHz)", "SF12 (125kHz)"]
    boundary = pd.DataFrame(all_sf.transpose(), columns=size, index=idx)
    boundary = boundary.transpose()

    cols = ["dimgrey", "red", "saddlebrown", "blue", "orange", "purple", "green", "black"]

    # Upper Boundary
    upper_b = list(repeat(14000,boundary.shape[0]))

    boundary.plot(ax=ax, linewidth=5,
                  color = cols)



    # Creating Fills
    ax.fill_between(boundary.index, boundary.iloc[:,0], boundary.iloc[:,1],
                    where=boundary.iloc[:,1] >= boundary.iloc[:,0], facecolor='dimgrey',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,1], boundary.iloc[:,2],
                    where=boundary.iloc[:,2] >= boundary.iloc[:,1], facecolor='red',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,2], boundary.iloc[:,3],
                    where=boundary.iloc[:,3] >= boundary.iloc[:,2], facecolor='saddlebrown',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,3], boundary.iloc[:,4],
                    where=boundary.iloc[:,4] >= boundary.iloc[:,3], facecolor='blue',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,4], boundary.iloc[:,5],
                    where=boundary.iloc[:,5] >= boundary.iloc[:,4], facecolor='orange',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,5], boundary.iloc[:,6],
                    where=boundary.iloc[:,6] >= boundary.iloc[:,5], facecolor='purple',
                    alpha=0.1)
    ax.fill_between(boundary.index, boundary.iloc[:,6], upper_b,
                    where=upper_b >= boundary.iloc[:,6], facecolor='green',
                    alpha=0.1)

    #posy, ytextvals = plt.yticks()
    #posx, xtextvals = plt.xticks()
    #plt.yticks(posy, boundary.index, rotation=0, fontsize=50, va="center")
    #plt.xticks(posx, , rotation=0, fontsize=50, va="top")


    devs = []
    devname = []
    for a, b in data.groupby("DevEUI or DevAddr", sort=False):
        if b.shape[0] > 1:
            for c, d in b.groupby(["bandwidth", "datarate"], sort=False):
                if d.shape[0] > 1:
                    if "-" in list(d.tx_interval[1:]):
                        error_idx = list(d.tx_interval[1:]).index("-")
                        new_tx = d.drop(d.index[error_idx+1])
                        new_dsize = d.drop(d.index[error_idx+1])
                        avg_tx = np.mean(new_tx.tx_interval[1:].apply(pd.to_numeric))
                        avg_size = np.mean(new_dsize["size"][1:].apply(pd.to_numeric))
                    else:
                        avg_tx = np.mean(d.tx_interval[1:].apply(pd.to_numeric))
                        avg_size = np.mean(d["size"][1:].apply(pd.to_numeric))
                else:
                    avg_tx = list(d.tx_interval)[0]
                    avg_size = list(d["size"])[0]
                stats = [int(float(c[0])/1000), c[1].strip(), avg_tx, avg_size]
            devname.append(a)
            devs.append(stats)

    devs = np.asarray(devs)

    # Assigning Colours
    col_l = []
    for i in devs:
        if (i[0] == "250") & (i[1] == "SF7"):
            col_l.append(cols[0])
        elif (i[0] == "125") & (i[1] == "SF7"):
            col_l.append(cols[1])
        elif (i[0] == "125") & (i[1] == "SF8"):
            col_l.append(cols[2])
        elif (i[0] == "125") & (i[1] == "SF9"):
            col_l.append(cols[3])
        elif (i[0] == "125") & (i[1] == "SF10"):
            col_l.append(cols[4])
        elif (i[0] == "125") & (i[1] == "SF11"):
            col_l.append(cols[5])
        elif (i[0] == "125") & (i[1] == "SF12"):
            col_l.append(cols[6])
        elif (i[0] == "500"):
            col_l.append(cols[7])

    # Plotting the Markers (Devices)
    plt.scatter(y=devs[:,2].astype(float), x=devs[:,3].astype(float),
                c=col_l,
                marker='x', s=500, linewidth=5)
    plt.ylim(0,14000)

    ax.tick_params(axis='both', which='major', pad=15)
    plt.ylim(0,14000)
    plt.xlabel("Packet Size [Bytes]", labelpad=15)
    plt.ylabel("Transmission Interval [s]", labelpad=30)
    plt.title("Observed device-wise transmission intervals against respective spectrum policy regions", pad=70, size=60)


if api_idx == 0:
    print(DeviceList())
elif api_idx == 1:
    print(ChannelOccupancy())
elif api_idx == 2:
    print(RSSI())
elif api_idx == 3:
    print(SNR())
elif api_idx == 4:
    print(NetworkList())
elif api_idx == 5:
    print(SpectrumPolicing())
