# LoRadar

![Overview of LoRaWAN communication and breakdown of LoRadar (Version 1)](https://drive.google.com/uc?export=view&id=1_DZtQ1pf7xVO5VPIY57kWERC9kML--kG)

## Introduction
LoRadar is a passive packet sniffing framework for LoRa built using off-the-shelf hardware. Unlike standard LoRaWAN gateways that relay the received LoRaWAN packets to the network server, LoRdar does not relay the received messages and is in essence an offline LoRaWAN gateway. This provides the benefit of not interfering with the existing network, such as changing the flow of the uplink and downlink packet transmissions.

## Versions
LoRadar supports all forms of LoRaWAN gateways, whether commercially purchased or custom-built. Support for commercially purchased gateways are based on using our Python script along with the gateways' built-in packet logging feature to collect the sniffed data. For custom-built gateways, LoRadar supports both SPI and USB-to-mPCIe connections. Data collection is achieved by using the packet logger developed by Jac Kersing (https://github.com/kersing/lora_gateway/tree/master/util_pkt_logger). We provide tutorials for three versions, below:
1) Version 1 (Custom-built; mTAC-LoRa as the module)
2) Version 2 (Custom-built; RAK831 as the module)
3) Version 3 (Commercial; Kerlink Wirnet Station)

## Data collection and information extraction
Once the data is collected, various sensor and network information are extracted from our python script, and outputed as a csv file:
- Unqiue device ID of each sensor
- Network server providers used
- Device manufacturers (for OTAA devices)
- Join-servers that authorized OTAA devices to join the network
- Type of messages received
- Transmission intervals for each device (per packet)
- Frame count of each transmission

The standards fields within a LoRaWAN packet, such as the data rate, code rate, and frequency channel are also displayed in the csv file.

## Visualization
