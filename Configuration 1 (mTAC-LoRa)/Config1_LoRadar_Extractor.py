### Libraries to load
import glob, matplotlib, pprint, requests, math, time, os
import pandas as pd
import numpy as np
from collections import Counter
from itertools import repeat
import matplotlib.pyplot as plt


### Loading the data
os.chdir = ("/home/pi/LoraWAN-Gateway/lora_gateway/util_pkt_logger")
docs = glob.glob(os.chdir + "/*.csv")

if len(docs) > 1:
    print("1. Reading " + str(len(docs)) + " csv files...")
    all_dat = []
    for doc in docs:
        all_dat.append(pd.read_csv(doc, encoding = 'unicode_escape'))

    every = pd.concat(all_dat)
    every.reset_index(inplace=True)
    every = every.dropna(subset=["UTC timestamp"])
    every = every.drop("index", axis=1)

elif len(docs) == 1:
    print("1. Reading one csv file...")
    print(docs)
    every = pd.read_csv(docs[0], encoding = 'unicode_escape')
    every.reset_index(inplace=True)
    every = every.dropna(subset=["UTC timestamp"])
    every = every.drop("index", axis=1)

elif len(docs) == 0:
    print("ERROR: No Data Files!")
    exit()


### Filtering the data for ABP
print("2. Filtering the data for ABP...")
info = every.payload
info = list(map(str, info)) # Convert payload to string. This is needed as some payloads only have integers.
devs = []
fcnts = []
mhdrs = []
fctrls = []
devaddr_revl = []
fcnt_revl = []
devaddr_len = 8

for i in info:
    devaddr = i[2:11].split("-")
    devaddr = "".join(devaddr)
    fcnt = i[13:17].split("-")
    fcnt = "".join(fcnt)
    fctrl = i[11:13].split("-")
    fctrl = "".join(fctrl)
    mhdr = i[:2].split("-")
    mhdr = "".join(mhdr)
    devs.append(devaddr)
    fcnts.append(fcnt)
    fctrls.append(fctrl)
    mhdrs.append(mhdr)

# reversing the little endian form of DevAddr and Fcnt
for row in devs:
    fixed = []
    for j in range(int(len(row)/2)):
        fixed.append(row[j*2:(j+1)*2])
    fixed.reverse()
    devaddr_rev = "".join(fixed)
    devaddr_revl.append(devaddr_rev)

for row in fcnts:
    fixed = []
    for j in range(int(len(row)/2)):
        fixed.append(row[j*2:(j+1)*2])
    fixed.reverse()
    fcnt_rev = "".join(fixed)
    fcnt_revl.append(fcnt_rev)

# Remove payloads shorter than the length of DevAddr, as these will not provide sufficient information to identify ABP devices
ttn_addr = []
all_addr = []
other_addr = []
network = []
activation = []
for addr in devaddr_revl:
    if len(addr) == devaddr_len:
        # Network prefix assignments to the World
        if addr[:2] == "26" or addr[:2] == "27":
            ttn_addr.append(addr) # potential DevAddr from TTN
            all_addr.append(addr)
            network.append("World: The Things Network")
            activation.append("ABP")
        elif addr[:2] == "04" or addr[:2] == "05":
            all_addr.append(addr)
            network.append("World: Actility")
            activation.append("ABP")
        elif addr[:2] == "10" or addr[:2] == "11":
            all_addr.append(addr)
            network.append("World: Orbiwise")
            activation.append("ABP")
        elif addr[:2] == "1a" or addr[:2] == "1b":
            all_addr.append(addr)
            network.append("World: SK Telecom")
            activation.append("ABP")
        elif addr[:2] == "1c" or addr[:2] == "1d":
            all_addr.append(addr)
            network.append("World: SagemCom")
            activation.append("ABP")
        elif addr[:2] == "24" or addr[:2] == "25":
            all_addr.append(addr)
            network.append("World: Kerlink")
            activation.append("ABP")
        elif addr[:2] == "2a" or addr[:2] == "2b":
            all_addr.append(addr)
            network.append("World: Cisco Systems")
            activation.append("ABP")
        elif addr[:2] == "2e" or addr[:2] == "2f":
            all_addr.append(addr)
            network.append("World: MultiTech Systems")
            activation.append("ABP")
        elif addr[:2] == "30" or addr[:2] == "31":
            all_addr.append(addr)
            network.append("World: Loriot")
            activation.append("ABP")
        elif addr[:2] == "32" or addr[:2] == "33":
            all_addr.append(addr)
            network.append("World: NNNCo")
            activation.append("ABP")
        elif addr[:2] == "34" or addr[:2] == "35":
            all_addr.append(addr)
            network.append("World: Flashnet")
            activation.append("ABP")
        elif addr[:2] == "36" or addr[:2] == "37":
            all_addr.append(addr)
            network.append("World: TrackNet")
            activation.append("ABP")
        elif addr[:2] == "38" or addr[:2] == "39":
            all_addr.append(addr)
            network.append("World: Lar.Tech")
            activation.append("ABP")
        elif addr[:2] == "3a" or addr[:2] == "3b":
            all_addr.append(addr)
            network.append("World: Swiss Led")
            activation.append("ABP")
        elif addr[:2] == "42" or addr[:2] == "43":
            all_addr.append(addr)
            network.append("World: Patavina Technologies")
            activation.append("ABP")
        elif addr[:2] == "48" or addr[:2] == "49":
            all_addr.append(addr)
            network.append("World: Gimasi")
            activation.append("ABP")
        elif addr[:2] == "4a" or addr[:2] == "4b":
            all_addr.append(addr)
            network.append("World: Talkpool")
            activation.append("ABP")
        elif addr[:2] == "4e" or addr[:2] == "4f":
            all_addr.append(addr)
            network.append("World: MCF88 SRL")
            activation.append("ABP")
        elif addr[:2] == "52" or addr[:2] == "53":
            all_addr.append(addr)
            network.append("World: GIoT")
            activation.append("ABP")
        elif addr[:2] == "54" or addr[:2] == "55":
            all_addr.append(addr)
            network.append("World: M2B Communications")
            activation.append("ABP")
        elif addr[:2] == "5a" or addr[:2] == "5b":
            all_addr.append(addr)
            network.append("World: Rai Way")
            activation.append("ABP")
        elif addr[:2] == "5c" or addr[:2] == "5d":
            all_addr.append(addr)
            network.append("World: Levikom")
            activation.append("ABP")
        elif addr[:2] == "60" or addr[:2] == "61":
            all_addr.append(addr)
            network.append("World: SoftBank")
            activation.append("ABP")
        elif addr[:2] == "62" or addr[:2] == "63":
            all_addr.append(addr)
            network.append("World: Inmarsat")
            activation.append("ABP")
        elif addr[:4] == "e006" or addr[:4] == "e007":
            all_addr.append(addr)
            network.append("World: IOTCAN")
            activation.append("ABP")
        elif addr[:4] == "e00a" or addr[:4] == "e00b":
            all_addr.append(addr)
            network.append("World: IoT Network AS")
            activation.append("ABP")
        elif addr[:4] == "e00e" or addr[:4] == "e00f":
            all_addr.append(addr)
            network.append("World: EDF")
            activation.append("ABP")
        elif addr[:4] == "e018" or addr[:4] == "e019":
            all_addr.append(addr)
            network.append("World: SenSys")
            activation.append("ABP")
        elif addr[:4] == "e01c" or addr[:4] == "e01d":
            all_addr.append(addr)
            network.append("World: Spark")
            activation.append("ABP")
        elif addr[:4] == "e020" or addr[:4] == "e021":
            all_addr.append(addr)
            network.append("World: Senet")
            activation.append("ABP")
        elif addr[:4] == "e026" or addr[:4] == "e027":
            all_addr.append(addr)
            network.append("World: Actility")
            activation.append("ABP")
        elif addr[:4] == "e02a" or addr[:4] == "e02b":
            all_addr.append(addr)
            network.append("World: Kerlink")
            activation.append("ABP")
        elif addr[:4] == "e02c" or addr[:4] == "e02d":
            all_addr.append(addr)
            network.append("World: Cisco")
            activation.append("ABP")
        elif addr[:4] == "e02e" or addr[:4] == "e02f":
            all_addr.append(addr)
            network.append("World: Schneider Electric")
            activation.append("ABP")
        elif addr[:4] == "e030" or addr[:4] == "e031":
            all_addr.append(addr)
            network.append("World: ZENNER")
            activation.append("ABP")
        elif addr[:4] == "e038" or addr[:4] == "e039":
            all_addr.append(addr)
            network.append("World: MachineQ/Comcast")
            activation.append("ABP")
        elif addr[:6] == "fc0004" or addr[:6] == "fc0005" or addr[:6] == "fc0006" or addr[:6] == "fc0007":
            all_addr.append(addr)
            network.append("World: Nordic Automation Systems")
            activation.append("ABP")
        elif addr[:6] == "fc0008" or addr[:6] == "fc0009" or addr[:6] == "fc000a" or addr[:6] == "fc000b":
            all_addr.append(addr)
            network.append("World: ResIOT")
            activation.append("ABP")
        elif addr[:6] == "fc000c" or addr[:6] == "fc000d" or addr[:6] == "fc000e" or addr[:6] == "fc000f":
            all_addr.append(addr)
            network.append("World: SYSDEV")
            activation.append("ABP")
        elif addr[:6] == "fc0020" or addr[:6] == "fc0021" or addr[:6] == "fc0022" or addr[:6] == "fc0023":
            all_addr.append(addr)
            network.append("World: Definium Technologies")
            activation.append("ABP")
        elif addr[:6] == "fc0030" or addr[:6] == "fc0031" or addr[:6] == "fc0032" or addr[:6] == "fc0033":
            all_addr.append(addr)
            network.append("World: nFore Technology")
            activation.append("ABP")
        elif addr[:6] == "fc0044" or addr[:6] == "fc0045" or addr[:6] == "fc0046" or addr[:6] == "fc0047":
            all_addr.append(addr)
            network.append("World: Digital Nordix AB (DNX)")
            activation.append("ABP")
        elif addr[:6] == "fc0058" or addr[:6] == "fc0059" or addr[:6] == "fc005a" or addr[:6] == "fc005b":
            all_addr.append(addr)
            network.append("World: Schneider Electric")
            activation.append("ABP")
        elif addr[:6] == "fc0060" or addr[:6] == "fc0061" or addr[:6] == "fc0062" or addr[:6] == "fc0063":
            all_addr.append(addr)
            network.append("World: ZENNER")
            activation.append("ABP")
        elif addr[:6] == "fc0068" or addr[:6] == "fc0069" or addr[:6] == "fc006a" or addr[:6] == "fc006b":
            all_addr.append(addr)
            network.append("World: REQUEA")
            activation.append("ABP")
        elif addr[:6] == "fc007c" or addr[:6] == "fc007d" or addr[:6] == "fc007e" or addr[:6] == "fc007f":
            all_addr.append(addr)
            network.append("World: mcf88 SRL")
            activation.append("ABP")
        elif addr[:6] == "fc0084" or addr[:6] == "fc0085" or addr[:6] == "fc0086" or addr[:6] == "fc0087":
            all_addr.append(addr)
            network.append("World: Hiber")
            activation.append("ABP")
        elif addr[:6] == "fc0098" or addr[:6] == "fc0099" or addr[:6] == "fc009a" or addr[:6] == "fc009b":
            all_addr.append(addr)
            network.append("World: Mirakonta")
            activation.append("ABP")
        
        # Network prefix assignments to Australia
        elif addr[:2] == "0a" or addr[:2] == "0b":
            all_addr.append(addr)
            network.append("Singapore Indonesia Australia Africa India: SingTel")
            activation.append("ABP")
        elif addr[:2] == "46" or addr[:2] == "47":
            all_addr.append(addr)
            network.append("Australia New Zealand: Ventia")
            activation.append("ABP")
        elif addr[:2] == "58" or addr[:2] == "59":
            all_addr.append(addr)
            network.append("Australia: Airlora")
            activation.append("ABP")
        
        # Neither
        else:
            all_addr.append(addr)
            other_addr.append(addr) # potential DevAddr from non-TTN network
            network.append("-")
            activation.append("-")
    else:
        all_addr.append("-")
        network.append("-")
        activation.append("-")
        


### Filtering the data for OTAA
print("3. Filtering the data for OTAA...")
info = every.payload
info = list(map(str, info))
deveuis = []
appeuis = []
deveui_revl = []
appeui_revl = []
deveui_len = 16
appeui_len = 16

for i in range(len(info)):
    if list(map(str, mhdrs))[i] == "00":
        deveui = info[i][20:38].split("-")
        deveui = "".join(deveui)
        appeui = info[i][2:20].split("-")
        appeui = "".join(appeui)
        deveuis.append(deveui)
        appeuis.append(appeui)
    else:
        deveuis.append("-")
        appeuis.append("-")

for row in deveuis: # reversing DevEUI's little endian form
    fixed = []
    for j in range(int(len(row)/2)):
        fixed.append(row[j*2:(j+1)*2])
    fixed.reverse()
    deveui_rev = "".join(fixed)
    deveui_revl.append(deveui_rev)

for row in appeuis: # reversing AppEUI's little endian form
    fixed = []
    for j in range(int(len(row)/2)):
        fixed.append(row[j*2:(j+1)*2])
    fixed.reverse()
    appeui_rev = "".join(fixed)
    appeui_revl.append(appeui_rev)

filt_deveui = [] # Remove payloads shorter than the length of DevAddr
filt_appeui = []
all_deveui = []
all_appeui = []
for deveui_s in deveui_revl:
    if len(deveui_s) == deveui_len:
        filt_deveui.append(deveui_s)
        all_deveui.append(deveui_s)
    else:
        all_deveui.append("-")

for appeui_s in appeui_revl:
    if len(appeui_s) == appeui_len:
        filt_appeui.append(appeui_s)
        all_appeui.append(appeui_s)
    else:
        all_appeui.append("-")
deveui_results = Counter(filt_deveui)
appeui_results = Counter(filt_appeui)



### Using API to obtain device manufacturer
print("4. Looking up device manufacturers...")
MAC_URL = "https://api.macvendors.com/v1/lookup/%s"
deveui_knowns = []
appeui_knowns = []
deveui_total = len(list(deveui_results.keys()))
appeui_total = len(list(appeui_results.keys()))

num = 1
starttime = time.time()
for eui in list(deveui_results.keys()):
    print("Looking up", num, "out of", deveui_total, "DevEUIs...")
    r = requests.get(MAC_URL % eui)
    if "data" in list(r.json().keys()):
        deveui_knowns.append([eui, r.json()])
    num += 1
    time.sleep(0.5)
    
num = 1
starttime = time.time()
for eui in list(appeui_results.keys()):
    print("Looking up", num, "out of", appeui_total, "AppEUIs...")
    r = requests.get(MAC_URL % eui)
    if "data" in list(r.json().keys()):
        appeui_knowns.append([eui, r.json()])
    num += 1
    time.sleep(0.5)
    


### Adding new columns
# Turn DevEUI and AppEUI knowns into dictionary
print("5. Adding new columns...")
deveui_knowns_dict = {}
appeui_knowns_dict = {}
for i in range(len(deveui_knowns)):
    deveui_knowns_dict[deveui_knowns[i][0]] = deveui_knowns[i][1]
for i in range(len(appeui_knowns)):
    appeui_knowns_dict[appeui_knowns[i][0]] = appeui_knowns[i][1]
    
# Get a list of devaddress and mic
devaddress = []
mic = []
for i in range(len(activation)):
    if activation[i] != "-":
        devaddress.append(devaddr_revl[i])
        if len("".join(info[i].split("-"))[-8:]) == 8:
            mic.append("".join(info[i].split("-"))[-8:])
        else:
            mic.append("-")
    else:
        devaddress.append(devaddr_revl[i])
        if len("".join(info[i].split("-"))[-8:]) == 8:
            mic.append("".join(info[i].split("-"))[-8:])
        else:
            mic.append("-")

# Create a dataframe for OTAA
dev_matcheui = []
app_matcheui = []
dev_manufeui = []
app_manufeui = []
manumac = []
for i in deveui_knowns:
    dev_matcheui.append(i[0])
    dev_manufeui.append(i[1].get("data").get("organization_name"))
    manumac.append(i[1].get("data").get("assignment"))

for i in appeui_knowns:
    app_matcheui.append(i[0])
    app_manufeui.append(i[1].get("data").get("organization_name"))

#manufdf = pd.DataFrame({"DevEUI": dev_matcheui, "DevManufacturer": dev_manufeui, "MAC_prefix": manumac,
#                        "AppEUI": app_matcheui, "AppManufacturer": app_manufeui})

dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
deveui_res = dictfilt(deveui_results, dev_matcheui)
appeui_res = dictfilt(appeui_results, app_matcheui)

# Update the new columns' values
dev_manufid = []
app_manufid = []
for i in range(len(all_deveui)):
    #if int(every["size"][i]) == 23 and str(mhdrs[i]) == "00":
    if (all_deveui[i] in dev_matcheui or all_appeui[i] in app_matcheui) and str(mhdrs[i]) == "00":
        activation[i] = "OTAA"
        network[i] = "-"
        devaddress[i] = all_deveui[i]
        if all_deveui[i] in dev_matcheui and all_appeui[i] in app_matcheui:
            dev_manufid.append(deveui_knowns_dict[all_deveui[i]].get("data").get("organization_name").replace(',', ''))
            app_manufid.append(appeui_knowns_dict[all_appeui[i]].get("data").get("organization_name").replace(',', ''))
        elif all_deveui[i] in dev_matcheui and all_appeui[i] not in app_matcheui:
            dev_manufid.append(deveui_knowns_dict[all_deveui[i]].get("data").get("organization_name").replace(',', ''))
            app_manufid.append("-")
        elif all_deveui[i] not in dev_matcheui and all_appeui[i] in app_matcheui:
            dev_manufid.append("-")
            app_manufid.append(appeui_knowns_dict[all_appeui[i]].get("data").get("organization_name").replace(',', ''))
        else:
            dev_manufid.append("-")
            app_manufid.append("-")
    elif int(every["size"][i]) == 23 and str(mhdrs[i]) == "00":
        activation[i] = "OTAA"
        network[i] = "-"
        devaddress[i] = all_deveui[i]
        if all_deveui[i] in dev_matcheui and all_appeui[i] in app_matcheui:
            dev_manufid.append(deveui_knowns_dict[all_deveui[i]].get("data").get("organization_name").replace(',', ''))
            app_manufid.append(appeui_knowns_dict[all_appeui[i]].get("data").get("organization_name").replace(',', ''))
        elif all_deveui[i] in dev_matcheui and all_appeui[i] not in app_matcheui:
            dev_manufid.append(deveui_knowns_dict[all_deveui[i]].get("data").get("organization_name").replace(',', ''))
            app_manufid.append("-")
        elif all_deveui[i] not in dev_matcheui and all_appeui[i] in app_matcheui:
            dev_manufid.append("-")
            app_manufid.append(appeui_knowns_dict[all_appeui[i]].get("data").get("organization_name").replace(',', ''))
        else:
            dev_manufid.append("-")
            app_manufid.append("-")
    else:
        dev_manufid.append("-")
        app_manufid.append("-")

all_fcnt = []
all_fctrl = []
all_mhdr = []
final_appeui = []
for i in range(len(activation)):
    if activation[i] == "ABP":
        final_appeui.append("-")
        all_mhdr.append(mhdrs[i])
        all_fcnt.append(fcnt_revl[i])
        all_fctrl.append(fctrls[i])
    elif activation[i] == "-":
        final_appeui.append("-")
        all_fcnt.append(fcnt_revl[i])
        all_fctrl.append(fctrls[i])
        all_mhdr.append(mhdrs[i])        
    elif activation[i] == "OTAA":
        final_appeui.append(all_appeui[i])
        all_fcnt.append("-")
        all_fctrl.append("-")
        all_mhdr.append(mhdrs[i])

# Converting MHDR (hex) to binary and getting message type
mtype_raw = []
for hexdec in all_mhdr:
    if hexdec == "-":
        mtype_raw.append("-")
    elif hexdec == "na":
        mtype_raw.append("-")
    elif hexdec == "9.":
        mtype_raw.append("-")
    else:
        scale = 16 ## equals to hexadecimal
        num_of_bits = 8
        mtype_raw.append(str(bin(int(hexdec, scale))[2:].zfill(num_of_bits)[:3]))

mtype_desc = []
for mtype in mtype_raw:
    if mtype == "000":
        mtype_desc.append("Join-request")
    elif mtype == "001":
        mtype_desc.append("Join-accept")
    elif mtype == "010":
        mtype_desc.append("Unconfirmed Data Up")
    elif mtype == "011":
        mtype_desc.append("Unconfirmed Data Down")
    elif mtype == "100":
        mtype_desc.append("Confirmed Data Up")
    elif mtype == "101":
        mtype_desc.append("Confirmed Data Down")
    elif mtype == "110":
        mtype_desc.append("Rejoin-request")
    elif mtype == "111":
        mtype_desc.append("Proprietary")
    else:
        mtype_desc.append("-")
        
# Converting fcnt (hex) to decimal       
int_fcnt = []
for fcnt_hex in all_fcnt:
    if str(fcnt_hex) == "-":
        int_fcnt.append("-")
    elif str(fcnt_hex) == "":
        int_fcnt.append("-")
    else:
        dec = int(fcnt_hex, 16)
        int_fcnt.append(dec)

# Correcting the time
yr = []
month = []
day = []
hrs = []
mins = []
secs = []
for i in list(every["UTC timestamp"]):
    #split for date and time
    date_split = i.split(" ")
    time_split = date_split[1].split(":")
    
    if int(date_split[0].split("-")[0]) == 2013:
        y = int(date_split[0].split("-")[0]) + 0
        if len(str(y)) == 1:
            yr.append("0"+str(y))
        else:
            yr.append(str(y))
        m = int(date_split[0].split("-")[1]) - 0
        if len(str(m)) == 1:
            month.append("0"+str(m))
        else:
            month.append(str(m))
        d = int(date_split[0].split("-")[2]) - 0
        if len(str(d)) == 1:
            day.append("0"+str(d))
        else:
            day.append(str(d))
        h = int(time_split[0]) + 0
        if len(str(h)) == 1:
            hrs.append("0"+str(h))
        else:
            hrs.append(str(h))
        m = int(time_split[1]) + 0
        if len(str(m)) == 1:
            mins.append("0"+str(m))
        else:
            mins.append(str(m))
        secs.append(time_split[2])
    
    elif int(date_split[0].split("-")[0]) == 2014:
        y = int(date_split[0].split("-")[0]) + 0
        if len(str(y)) == 1:
            yr.append("0"+str(y))
        else:
            yr.append(str(y))
        m = int(date_split[0].split("-")[1]) + 0
        if len(str(m)) == 1:
            month.append("0"+str(m))
        else:
            month.append(str(m))
        d = int(date_split[0].split("-")[2]) + 0
        if len(str(d)) == 1:
            day.append("0"+str(d))
        else:
            day.append(str(d))
        h = int(time_split[0]) + 0
        if len(str(h)) == 1:
            hrs.append("0"+str(h))
        else:
            hrs.append(str(h))
        m = int(time_split[1]) + 0
        if len(str(m)) == 1:
            mins.append("0"+str(m))
        else:
            mins.append(str(m))
        secs.append(time_split[2])
   
    else:
        yr.append(date_split[0].split("-")[0])
        month.append(date_split[0].split("-")[1])
        day.append(date_split[0].split("-")[2])
        h = int(time_split[0]) + 0
        if len(str(h)) == 1:
            hrs.append("0"+str(h))
        else:
            hrs.append(str(h))
        mins.append(time_split[1])
        secs.append(time_split[2])

yr = list(map(str, yr))
month = list(map(str, month))
day = list(map(str, day))
hrs = list(map(str, hrs))
mins = list(map(str, mins))
secs = list(map(str, secs))

# correcting cases where mins >= 60 and hours >= 24
for i in range(len(mins)):
    if int(mins[i]) >= 60:
        h = int(hrs[i])
        h += 1
        if len(str(h)) == 1:
            hrs[i] = "0"+str(h)
        else:
            hrs[i] = str(h)
        m = int(mins[i])
        m -= 60
        if len(str(m)) == 1:
            mins[i] = "0"+str(m)
        else:
            mins[i] = str(m)

for i in range(len(hrs)):
    if int(hrs[i]) >= 24:
        d = int(day[i])
        d += 1
        if len(str(d)) == 1:
            day[i] = "0"+str(d)
        else:
            day[i] = str(d)
        h = int(hrs[i])
        h -= 24
        if len(str(h)) == 1:
            hrs[i] = "0"+str(h)
        else:
            hrs[i] = str(h)

# correcting cases where day is > possible value within a certain month
for i in range(len(day)):
    if int(day[i]) > 30:
        if month[i] in ["4", "6", "9", "11"]:
            m = int(month[i])
            m += 1
            if len(str(m)) == 1:
                month[i] = "0"+str(m)
            else:
                month[i] = str(m)
            d = int(day[i])
            d -= 30
            if len(str(d)) == 1:
                day[i] = "0"+str(d)
            else:
                day[i] = str(d)
    elif int(day[i]) > 28:
        if month[i] in ["2"]:
            if int(yr[i])%4 == 0 and int(day[i]) > 29:
                m = int(month[i])
                m += 1
                if len(str(m)) == 1:
                    month[i] = "0"+str(m)
                else:
                    month[i] = str(m)
                d = int(day[i])
                d -= 29
                if len(str(d)) == 1:
                    day[i] = "0"+str(d)
                else:
                    day[i] = str(d)
            elif int(yr[i])%4 != 0:
                m = int(month[i])
                m += 1
                if len(str(m)) == 1:
                    month[i] = "0"+str(m)
                else:
                    month[i] = str(m)
                d = int(day[i])
                d -= 28
                if len(str(d)) == 1:
                    day[i] = "0"+str(d)
                else:
                    day[i] = str(d)

# correcting cases where year needs to be changed
for i in range(len(month)):
    if int(month[i]) == 12 and int(day[i]) > 31:
        y = int(yr[i])
        y += 1
        yr[i] = str(y)
        m = 1
        if len(str(m)) == 1:
            month[i] = "0"+str(m)
        else:
            month[i] = str(m)
        d = 1
        if len(str(d)) == 1:
            day[i] = "0"+str(d)
        else:
            day[i] = str(d)

# concatenating the fixed date time
date = []
aus_time = []

for i in range(len(yr)):
    date.append("-".join([yr[i], month[i], day[i]]))
    aus_time.append(":".join([hrs[i], mins[i], secs[i]]))

every["date"] = date
every["time"] = aus_time
every["activation"] = activation
every["network"] = network
every["DevEUI or DevAddr"] = devaddress
every["AppEUI"] = final_appeui
every["fctrl"] = all_fctrl
every["fcnt"] = int_fcnt
every["mhdr"] = all_mhdr
every["mtype"] = mtype_raw
every["mtype_desc"] = mtype_desc
every["MIC"] = mic
every["deveui_manufacturer"] = dev_manufid
every["appeui_manufacturer"] = app_manufid

every = every[['UTC timestamp', 'date', 'time', 'us count', 'frequency', 'RF chain', 'RX chain','status',
               'bandwidth', 'datarate', 'coderate', 'RSSI', 'SNR', 'size', 'DevEUI or DevAddr',
               'AppEUI', 'fctrl', 'fcnt', 'mhdr', 'mtype', 'mtype_desc', 'MIC', 'activation',
               'network', 'deveui_manufacturer', 'appeui_manufacturer', 'payload']]

filtered = every.copy()
no_fcnt = filtered.loc[(filtered.fcnt == "-") & (filtered.activation != "OTAA")].index
filtered = filtered.drop(no_fcnt)



### Calculating the time difference
# Function for truncating decimals without rounding to 3 dp
print("6. Calculating the time difference in seconds...")
time_sec = []
timeutc = list(pd.to_datetime(filtered["UTC timestamp"]))
for i in range(len(timeutc)):
    time_sec.append(pd.Timedelta(timeutc[i]-timeutc[0]).total_seconds())

# Add a new column to the dataframe
filtered["sec_diff"] = time_sec



### Algorithm for identifying unique devices
# Split it from the original dataframe by DevAddr or DevEUI
print("7. Identifying unique devices...")
l_freq = []
l_devaddr915 = []
l_devaddr923 = []
all_freq = []
filtered = filtered.loc[filtered.status == "CRC_OK "]

# ISM band
fr915 = [916800000, 917000000, 917200000, 917400000, 917600000, 917800000, 918000000, 91820000]
fr923 = [922000000, 922100000, 922200000, 922400000, 922600000, 922800000, 923000000, 923200000, 923400000]

freq915 = filtered.loc[filtered.frequency.isin(fr915)]
if freq915.shape[0] > 0:
    freq915 = filtered.loc[filtered.frequency.isin(fr915)].index
    filtered.loc[freq915, "Freq_Plan"] = "915band"
    all_freq.append(freq915)

freq923 = filtered.loc[filtered.frequency.isin(fr923)]
if freq923.shape[0] > 0:
    freq923 = filtered.loc[filtered.frequency.isin(fr923)].index
    filtered.loc[freq923, "Freq_Plan"] = "923band"
    all_freq.append(freq923)

if len(all_freq) == 0:
    print("ERROR: No valid LoRaWAN packets!")
    exit()

if (freq915.shape[0] and freq923.shape[0]) > 0:
    for a, b in filtered.groupby("Freq_Plan", sort=False):
        l_freq.append(b.sort_values(by=["sec_diff"]))
    #915
    for a, b in l_freq[0].groupby("DevEUI or DevAddr", sort=False):
        l_devaddr915.append(b.sort_values(by=["sec_diff"]))
    #923
    for a, b in l_freq[1].groupby("DevEUI or DevAddr", sort=False):
        l_devaddr923.append(b.sort_values(by=["sec_diff"]))

elif freq915.shape[0] == 0:
    #923
    for a, b in filtered.groupby("DevEUI or DevAddr", sort=False):
        l_devaddr923.append(b.sort_values(by=["sec_diff"]))

elif freq923.shape[0] == 0:
    #915
    for a, b in filtered.groupby("DevEUI or DevAddr", sort=False):
        l_devaddr915.append(b.sort_values(by=["sec_diff"]))


### Counting the number of devices
print("8. Counting the number of devices...")
def truncate(f):
    if f == "-":
        return "-"
    else:
        return math.floor(f * 10 ** 3) / 10 ** 3

def truncate3(f):
    if f == "-":
        return "-"
    else:
        return math.floor(f * 10 ** 3) / 10 ** 3

def truncate0(f):
    if f == "-":
        return "-"
    else:
        return math.floor(f * 10 ** 0) / 10 ** 0

dev_num915 = []
rate915 = []
dev_num923 = []
rate923 = []
num = 1
    
# Identifying unique devices
l_index_915 = []
if len(l_devaddr915) > 0:
    for i in l_devaddr915:   
        sec_df = list(map(float, i["sec_diff"]))
        sec_df = [x - sec_df[0] for x in sec_df]
        sec_df = list(map(truncate, sec_df))
            
        devaddr_df = list(i["DevEUI or DevAddr"])
        activation_df = list(i["activation"])
           
        # OTAA case
        if activation_df[0] == "OTAA":
            l_index_915.extend(i.index)
            for j in range(len(devaddr_df)):
                if j >= 1:
                    rate915.append(truncate3(float(sec_df[j]) - float(sec_df[j-1])))
                else:
                    rate915.append("-")
            dev_num915.extend(repeat(num, len(devaddr_df)))
            num += 1
            
        # ABP case
        # Single packet case
        elif i.shape[0] == 1 and activation_df[0] != "OTAA":
            l_index_915.extend(i.index)
            dev_num915.append(num)
            rate915.append("-")
            num += 1
        
        # 2 packets or more
        elif i.shape[0] > 1 and activation_df[0] == "ABP":
            dev_num915.extend(repeat(num, i.shape[0]))
            #j = i.sort_values(by=["date", "time"]) # sort by date and time
            l_index_915.extend(i.index)
            fcnt_df = list(map(int, i["fcnt"]))
            i_rate = []
            rate915.append("-")
            
            for k in range(len(fcnt_df)): # +1 to start from 2nd row
                if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                    if fcnt_df[k] != fcnt_df[k-1]:
                        i_rate.append(truncate3(((sec_df[k] - sec_df[k-1])/(fcnt_df[k] - fcnt_df[k-1]))))
                    else:
                        i_rate.append(truncate3((sec_df[k] - sec_df[k-1])))
            trunc_i_rate = []
            i_rate2 = list(map(np.round, i_rate))
            i_rate_set = list(dict.fromkeys(i_rate2)) # list of the set intervals to look up for assigning devnumber
            # Remove rates that are within +-1 rate of each other
            for m in range(len(i_rate_set)):
                if m == 0:
                    trunc_i_rate.append(i_rate_set[m])
                elif m >= 1:
                    if (i_rate_set[m] > all([x+1 for x in trunc_i_rate])) or (i_rate_set[m] < all([x-1 for x in trunc_i_rate])):
                        trunc_i_rate.append(i_rate_set[m])                 
                
            for element in i_rate:
                for i_devnum in range(len(trunc_i_rate)):
                    if (trunc_i_rate[i_devnum] - 1) <= float(element) <= (trunc_i_rate[i_devnum] + 1):
                        break
                    else:
                        continue
                rate915.append(element)
            num += 1
        
        # For neither OTAA and ABP activation and more than 1 packet
        elif i.shape[0] > 1 and activation_df[0] == "-":
            dev_num915.extend(repeat(num, i.shape[0]))
            #j = i.sort_values(by=["date", "time"]) # sort by date and time
            l_index_915.extend(i.index)
            fcnt_df = list(i["fcnt"])
            if any(i["fcnt"] == "-"):
                for k in range(len(fcnt_df)): # +1 to start from 2nd row
                    if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                        rate915.append(truncate3((sec_df[k] - sec_df[k-1])))
            else:
                fcnt_df = list(map(int, i["fcnt"]))
                i_rate = []
                rate915.append("-")

                for k in range(len(fcnt_df)): # +1 to start from 2nd row
                    if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                        if fcnt_df[k] != fcnt_df[k-1]:
                            i_rate.append(truncate3(((sec_df[k] - sec_df[k-1])/(fcnt_df[k] - fcnt_df[k-1]))))
                        else:
                            i_rate.append(truncate3((sec_df[k] - sec_df[k-1])))
                trunc_i_rate = []
                i_rate2 = list(map(np.round, i_rate))
                i_rate_set = list(dict.fromkeys(i_rate2)) # list of the set intervals to look up for assigning devnumber
                # Remove rates that are within +-1 rate of each other
                for m in range(len(i_rate_set)):
                    if m == 0:
                        trunc_i_rate.append(i_rate_set[m])
                    elif m >= 1:
                        if (i_rate_set[m] > all([x+1 for x in trunc_i_rate])) or (i_rate_set[m] < all([x-1 for x in trunc_i_rate])):
                            trunc_i_rate.append(i_rate_set[m])                   

                for element in i_rate:
                    for i_devnum in range(len(trunc_i_rate)):
                        if (trunc_i_rate[i_devnum] - 1) <= float(element) <= (trunc_i_rate[i_devnum] + 1):
                            break
                        else:
                            continue
                    rate915.append(element)
            num += 1
    
l_index_923 = []
if len(l_devaddr923) > 0:
    for i in l_devaddr923:   
        sec_df = list(map(float, i["sec_diff"]))
        sec_df = [x - sec_df[0] for x in sec_df]
        sec_df = list(map(truncate, sec_df))
            
        devaddr_df = list(i["DevEUI or DevAddr"])
        activation_df = list(i["activation"])
           
        # OTAA case
        if activation_df[0] == "OTAA":
            l_index_923.extend(i.index)
            for j in range(len(devaddr_df)):
                if j >= 1:
                    rate923.append(truncate3(float(sec_df[j]) - float(sec_df[j-1])))
                else:
                    rate923.append("-")
            dev_num923.extend(repeat(num, len(devaddr_df)))
            num += 1
            
        # ABP case
        # Single packet case
        elif i.shape[0] == 1 and activation_df[0] != "OTAA":
            l_index_923.extend(i.index)
            dev_num923.append(num)
            rate923.append("-")
            num += 1
        
        # 2 packets or more
        elif i.shape[0] > 1 and activation_df[0] == "ABP":
            dev_num923.extend(repeat(num, i.shape[0]))
            #j = i.sort_values(by=["date", "time"]) # sort by date and time
            l_index_923.extend(i.index)
            fcnt_df = list(map(int, i["fcnt"]))
            i_rate = []
            rate923.append("-")
            
            for k in range(len(fcnt_df)): # +1 to start from 2nd row
                if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                    if fcnt_df[k] != fcnt_df[k-1]:
                        i_rate.append(truncate3(((sec_df[k] - sec_df[k-1])/(fcnt_df[k] - fcnt_df[k-1]))))
                    else:
                        i_rate.append(truncate3((sec_df[k] - sec_df[k-1])))
            trunc_i_rate = []
            i_rate2 = list(map(np.round, i_rate))
            i_rate_set = list(dict.fromkeys(i_rate2)) # list of the set intervals to look up for assigning devnumber
            # Remove rates that are within +-1 rate of each other
            for m in range(len(i_rate_set)):
                if m == 0:
                    trunc_i_rate.append(i_rate_set[m])
                elif m >= 1:
                    if (i_rate_set[m] > all([x+1 for x in trunc_i_rate])) or (i_rate_set[m] < all([x-1 for x in trunc_i_rate])):
                        trunc_i_rate.append(i_rate_set[m])                 
                
            for element in i_rate:
                for i_devnum in range(len(trunc_i_rate)):
                    if (trunc_i_rate[i_devnum] - 1) <= float(element) <= (trunc_i_rate[i_devnum] + 1):
                        break
                    else:
                        continue
                rate923.append(element)      
            num += 1
        
        # For neither OTAA and ABP activation and more than 1 packet
        elif i.shape[0] > 1 and activation_df[0] == "-":
            dev_num923.extend(repeat(num, i.shape[0]))
            #j = i.sort_values(by=["date", "time"]) # sort by date and time
            l_index_923.extend(i.index)
            fcnt_df = list(i["fcnt"])
            if any(i["fcnt"] == "-"):
                for k in range(len(fcnt_df)): # +1 to start from 2nd row
                    if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                        rate923.append(truncate3((sec_df[k] - sec_df[k-1])))
            else:
                fcnt_df = list(map(int, i["fcnt"]))
                i_rate = []
                rate923.append("-")

                for k in range(len(fcnt_df)): # +1 to start from 2nd row
                    if 1 <= k < len(fcnt_df): # make sure it doesn't exceed the row index limit
                        if fcnt_df[k] != fcnt_df[k-1]:
                            i_rate.append(truncate3(((sec_df[k] - sec_df[k-1])/(fcnt_df[k] - fcnt_df[k-1]))))
                        else:
                            i_rate.append(truncate3((sec_df[k] - sec_df[k-1])))
                trunc_i_rate = []
                i_rate2 = list(map(np.round, i_rate))
                i_rate_set = list(dict.fromkeys(i_rate2)) # list of the set intervals to look up for assigning devnumber
                # Remove rates that are within +-1 rate of each other
                for m in range(len(i_rate_set)):
                    if m == 0:
                        trunc_i_rate.append(i_rate_set[m])
                    elif m >= 1:
                        if (i_rate_set[m] > all([x+1 for x in trunc_i_rate])) or (i_rate_set[m] < all([x-1 for x in trunc_i_rate])):
                            trunc_i_rate.append(i_rate_set[m])                   

                for element in i_rate:
                    for i_devnum in range(len(trunc_i_rate)):
                        if (trunc_i_rate[i_devnum] - 1) <= float(element) <= (trunc_i_rate[i_devnum] + 1):
                            break
                        else:
                            continue
                    rate923.append(element)
            num += 1
    


### Sort the derived device number, interval, rate by their corresponding index (to match it with original dataframe)
print("9. Sorting the device numbers by index...")
def sortFirst(val): 
    return val[0]

all_l_indx = []
rate = []
dev_num = []

if len(l_devaddr915) > 0:
    all_list915 = list(zip(l_index_915, rate915, dev_num915))
    all_list915.sort(key = sortFirst)

    for i in all_list915:
        all_l_indx.append(i[0])
        rate.append(i[1])
        dev_num.append(i[2])

elif len(l_devaddr) > 0:
    all_list923 = list(zip(l_index_923, rate923, dev_num923))
    all_list923.sort(key = sortFirst)
    
    for i in all_list923:
        all_l_indx.append(i[0])
        rate.append(i[1])
        dev_num.append(i[2])
    
all_list = list(zip(all_l_indx, rate, dev_num))
all_list.sort(key = sortFirst)


### Adding the corrected ordered tx_interval and dev_number to the dataframe
print("10. Adding the transmission interval column...")
l_rate = []
l_dev_num = []
for i in all_list:
    if i[1] != "-":
        l_rate.append(float(i[1]))
        l_dev_num.append(int(i[2]))
    else:
        l_rate.append(i[1])
        l_dev_num.append(int(i[2]))
    
filtered["tx_interval"] = l_rate
filtered["dev_number"] = l_dev_num



### Save as csv
print("11. Saving as csv...")
filtered.to_csv(pd.datetime.today().strftime('%y%m%d_%H%M%S_') + "LoRadar_data.csv", index=False)
print("Data saved!")
