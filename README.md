# _LoRadar_

![Overview of LoRaWAN communication and breakdown of LoRadar (Version 1).](https://drive.google.com/uc?export=view&id=1MKsdDbceHVgKC9ZMwL1FuyNo4fZK0WaD)

## Introduction
LoRa is the physical layer access technology that employs a variant of the chirp spreadspectrum modulation, allowing low powered transmission of small data rates (0.3 kbps to 50 kbps) over a long distances (up to 15 km in suburban and 2 km in dense urban areas). LoRaWAN is a star topology network architecture developed on top of LoRa physical layer for communication between a gateway and an IoT sensor.

_LoRadar_ is a passive packet sniffing framework for LoRa built using off-the-shelf hardware. Unlike standard LoRaWAN gateways that relay the received LoRaWAN packets to the network server, _LoRdar_ does not relay the received messages and is in essence an offline LoRaWAN gateway. This provides the benefit of not interfering with the existing network, such as changing the flow of the uplink and downlink packet transmissions.

## Versions

![Summary of the LoRadar versions.](https://drive.google.com/uc?export=view&id=1OKXoblexwRSbd8lldo-9EEsxAR2Xif-K)

_LoRadar_ supports all forms of LoRaWAN gateways, whether commercially purchased or custom-built. Support for commercially purchased gateways are based on using our Python script along with the gateways' built-in packet logging feature to collect the sniffed data. For custom-built gateways, LoRadar supports both SPI and USB-to-mPCIe connections. Data collection is achieved by using the packet logger developed by Jac Kersing (https://github.com/kersing/lora_gateway/tree/master/util_pkt_logger). We provide tutorials for three versions below:
1) Version 1 (Custom-built; mTAC-LoRa as the module)
2) Version 2 (Custom-built; RAK831 as the module)
3) Version 3 (Commercial; Kerlink Wirnet Station)

Instructions for each version are provided in their corresponding directory.

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
The extracted information can also be visualized on a web dashboard, through Kibana from the Elasticsearch-Logstash-Kibana (ELK) stack. Instructions on installing and setting up the Kibana dashboard is found in the 'Kibana' directory.

![A screenshot of the Kibana dashboard.](https://drive.google.com/uc?export=view&id=1sM8tS8UqK4CDGhlQFkQ7e9hJQtHtDFv5)
