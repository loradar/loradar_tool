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

Description of the fields in the csv file are shown below.

| Field Name | Description |
| :---       | :---        |
| UTC timestamp | UTC time of receiving LoRaWAN packet. |
| date | Date within UTC timestamp. |
| time | Time within UTC timesatmp. |
| us count | The value of the gateway internal time counter at the instant the LoRaWAN packet was received, in microseconds. The value rolls over every 72 minutes. |
| frequency | Center frequency of the received signal in MHz. |
| RF chain | Radio frequency chain receiving the LoRaWAN packet. |
| RX chain | Intermediate Frequency channel used to receive the packet. |
| status | The result of the gateway's CRC test on the frame. |
| bandwidth | Bandwidth of the LoRaWAN packet in kHz. |
| datarate | Spreading factor of the LoRaWAN packet. |
| coderate | The ratio of carried bits and total number of bits received. |
| RSSI | Received siganl strength of the packet in dBm. |
| SNR | Signal to noise ratio of the LoRaWAN packet. |
| size | The number of octets in the packet. |
| DevEUI or DevAddr | EUI or address of the device that the packet was sent by. |
| AppEUI | (JoinEUI in LoRaWAN specs v1.1) The EUI of the join-server that authorized the join request. |
| fctrl | Frame control value (raw). |
| fcnt | Frame count number (converted). |
| mhdr | MAC Header (raw). |
| mtype | Message type extracted from MAC Header (raw). |
| mtype_desc | Message type extracted from MAC Header (converted). |
| MIC | 4-octet message integrity code. |
| activation | Activation method. |
| network | Network that the device of the packet belongs to. |
| deveui_manufacturer | Manufacturer of the OTAA device. |
| appeui_manufacturer | Join-server that authorized the join request. |
| payload | PHY payload of the LoRaWAN packet. |
| sec_diff | Time differential from previous packet, in seconds. |
| Freq_Plan | The frequency bandplan the device is using. |
| tx_interval | Approximated transmission interval per packet for the device, based on frame count. |
| dev_number | Number assigned to the unique device. |

## Visualization
The extracted information can also be visualized on a web dashboard, through Kibana from the Elasticsearch-Logstash-Kibana (ELK) stack. Instructions on installing and setting up the Kibana dashboard are found in the 'Kibana' directory.

![A screenshot of the Kibana dashboard.](https://drive.google.com/uc?export=view&id=1sM8tS8UqK4CDGhlQFkQ7e9hJQtHtDFv5)

## APIs
LoRadar provides support for various information extraction requests through its Python script of executable functions. It uses the data file output from the scan and shows the results of the executed function in JSON format. Instructions on the APIs are found in the 'APIs' directory.
