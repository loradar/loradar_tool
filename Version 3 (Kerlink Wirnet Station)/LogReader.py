#Please update 'GatewayID' to unique ID of the LoRa gateway
GatewayID='0'
import csv
from base64 import b64decode
from textwrap import wrap
import os
import glob
NumFiles = len(glob.glob1('',"*.log'"))
for numberrand in range(NumFiles):
    #print(numberrand)
    qwe=str(numberrand)
    filename="'LoRaMacServer ("+qwe+").log'"
    if numberrand==0:
        filename="'LoRaMacServer.log'"
    f = open(filename)
    i=0
    for each in f:
        each=each.split(' ')
        if len(each)>7 and each[7]=="JSON" and each[10][2:6]=="rxpk":
            i+=1
            month=['te','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            UTC_timestamp=each[6][:-1]+"-"+str(month.index(each[5]))+"-"+each[4]+" "+each[0]+"."+each[2]
            data=each[10][10:-5].split(",")    
            for item in range(len(data)):
                data[item]=data[item].split(":")
            for item,value in data:
                if item=='"tmst"':
                    us_count=value
                elif item=='"chan"':
                    RX_chain=value
                elif item=='"rfch"':
                    RF_chain=value
                elif item=='"freq"':
                    frequency=str(float(value)*1000000)
                elif item=='"stat"':
                    status=["CRC_BAD","CRC_OK"][int(value)]
                elif item=='"modu"':
                    modulation=value[1:-1]
                elif item=='"datr"':
                    tempdr=value[1:-1]
                    tempdr2=tempdr.find('BW')
                    datarate=tempdr[:tempdr2]
                    bandwidth=tempdr[tempdr2+2:]+"000"
                elif item=='"codr"':
                    coderate=value[1:-1]  #there might be a problem here
                elif item=='"lsnr"':
                    SNR=value
                elif item=='"rssi"':
                    RSSI=value
                elif item=='"size"':
                    size=value
                elif item=='"data"':
                    pdataa=value[1:]
                    pdataa="aaaa"+pdataa
                    pdataaa=(str(hex(int.from_bytes(b64decode(pdataa), 'big')))[2:]).upper()
                    pdata='-'.join(wrap(pdataaa[6:], 8)) 
            with open(r'data.csv', 'a', newline='') as csvfile:
                fieldnames = ['gateway ID','node MAC','UTC timestamp','us count','frequency','RF chain','RX chain','status','size','modulation','bandwidth','datarate','coderate','RSSI','SNR','payload']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'gateway ID':GatewayID,'node MAC':'0','UTC timestamp':UTC_timestamp,'us count':us_count,'frequency':frequency,'RF chain':RF_chain,'RX chain':RX_chain,'status':status,'size':size,'modulation':modulation,'bandwidth':bandwidth,'datarate':datarate,'coderate':coderate,'RSSI':RSSI,'SNR':SNR,'payload':pdata})
from more_itertools import unique_everseen
with open('data.csv','r') as f, open('Packets.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
os.remove("data.csv")
with open('Packets.csv','r') as contents:
      save = contents.read()
with open('Packets.csv','w') as contents:
      contents.write('gateway ID,node MAC,UTC timestamp,us count,frequency,RF chain,RX chain,status,size,modulation,bandwidth,datarate,coderate,RSSI,SNR,payload'+'\n')
with open('Packets.csv','a') as contents:
      contents.write(save)