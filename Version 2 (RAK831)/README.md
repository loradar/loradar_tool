# _LoRadar_ (Version 2)

## Hardware used
This version setup uses the following hardware:
- **Single board computer:** Raspberry Pi 3
- **LoRa module:** RAK831, a gateway accessory from RAK wireless suitable for both 915 MHz and 923 MHz ISM frequency bands was used to capture LoRa packets
- **Antenna:** A fibreglass 1/2 wave 860-960 MHz antenna with 2 dBi gain attached to the LoRa module
- **Connection bridge:** Mini PCI-e to USB adaptor to connect between the Raspberry Pi and mTAC-LORA-915A (https://techship.com/products/mpcie-to-usb-adapter-card/)
- **Storage:** 32 GB microSD card inserted to the Raspberry Pi for data storage

## Software used
- **libloragw library:** (https://github.com/Lora-net/lora_gateway/tree/master/libloragw) was used for the Raspberry Pi to access the LoRa card and configure radio frequencies
- **Packet logger:** (https://github.com/Lora-net/lora_gateway/tree/master/util_pkt_logger) This software records all LoRa packets received by the LoRa card and outputs in csv format every hour.

*The Raspberry Pi has been configured to initiate the 'Packet logger software' upon powering on and obtaining the correct time via the Internet (A delay of 5 minutes has been placed).

## Instructions
