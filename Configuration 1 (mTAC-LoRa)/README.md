# _LoRadar_ (Configuration 1)

## Hardware used
This configuration setup uses the following hardware:
- **Single board computer:** Raspberry Pi 3
- **LoRa module:** mTAC-LORA-915 (not mTAC-LORA-915-H), a gateway accessory card from MultiTech suitable for both 915 MHz and 923 MHz ISM frequency bands was used to capture LoRa packets
- **Antenna:** A fibreglass 1/2 wave 860-960 MHz antenna with 6 dBi gain attached to the LoRa module via _N-type (male) to RP-SMA (male) cable_ (https://www.data-alliance.net/n-male-to-rp-sma-male-cable-3ft-5ft-6ft-lmr-100-lmr200-double-shielded/)
- **Connection bridge:** Mini PCI-e to USB adaptor to connect between the Raspberry Pi and mTAC-LORA-915A (https://techship.com/products/mpcie-to-usb-adapter-card/)
- **Storage:** 32 GB microSD card inserted to the Raspberry Pi for data storage

## Software used
- **libloragw library:** (https://github.com/Lora-net/lora_gateway/tree/master/libloragw) was used for the Raspberry Pi to access the LoRa card and configure radio frequencies
- **Packet logger:** (https://github.com/Lora-net/lora_gateway/tree/master/util_pkt_logger) This software records all LoRa packets received by the LoRa card and outputs in csv format every hour.

*The Raspberry Pi has been configured to initiate the 'Packet logger software' upon powering on and obtaining the correct time via the Internet (A delay of 5 minutes has been placed).*

## Instructions
1) Download the Raspberry Pi (RPi) image according to the frequency bandplan of interest:  
- 915 frequency: https://drive.google.com/file/d/144UO2tI30Df7-DTuJlAsTuzdEE44IgZ3/view?usp=sharing
- 923 frequency: https://drive.google.com/file/d/1Wxu4gwcrQ9sh8w0kbiSxsRnPNqzYcCHC/view?usp=sharing
2) Flash the image onto an SD card, using _balenaEtcher_ (https://www.balena.io/etcher/)
3) Insert the SD card into the RPi and power it on, and the data collection should commence in 5 minutes (It is recommended that you connect the RPi to a wired or wireless network so that the correct time can be obtained)

## Information extraction (Requires Internet Connection)
To extract the information, follow the steps below:
1) Download the _Config1\_LoRadar\_Extractor.py_ python script from above and place it in the _Downloads_ folder of the Raspberry Pi
2) Open a terminal and enter the following commands to install the required libraries:  
`sudo apt-get install python3-matplotlib --assume-yes`  
`sudo apt-get install python3-pandas --assume-yes`
3) Open the python script with _Python 3 (IDLE)_
4) Run the module (Requires Internet Connection)
5) Upon successful extraction, a csv file will be created in the same directory as the _Ver1\_LoRadar\_Extractor.py_ python script
