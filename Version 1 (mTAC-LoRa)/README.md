# _LoRadar_ (Version 1)

## Hardware used
This version setup uses the following hardware:
- **Single board computer:** Raspberry Pi 3
- **LoRa module:** mTAC-LORA-915 (not mTAC-LORA-915-H), a gateway accessory card from MultiTech suitable for both 915 MHz and 923 MHz ISM frequency bands was used to capture LoRa packets
- **Antenna:** A fibreglass 1/2 wave 860-960 MHz antenna with 6 dBi gain attached to the LoRa module via _N-type (male) to RP-SMA (male) cable_ (https://www.data-alliance.net/n-male-to-rp-sma-male-cable-3ft-5ft-6ft-lmr-100-lmr200-double-shielded/)
- **Connection bridge:** mini PCI-e to USB adaptor to connect between the Raspberry Pi and mTAC-LORA-915A (https://techship.com/products/mpcie-to-usb-adapter-card/)
- **Storage:** 32 GB microSD card inserted to the Raspberry Pi for data storage

## Software used
The libloragw library [7] was used for the Raspberry Pi to access the LoRa card and configure radio frequencies. The 922.0-923.4 MHz band-plan setting was selected for 923 MHz, while sub-band 2 was selected for the 915 MHz ISM band based on their popularity among network providers in the country of interest. On top of the library, data collection was conducted through a LoRa packet logger software [8] which records all LoRa packets received by the LoRa card. This was chosen for the convenience of not having to register the gateway to a particular network server and its csv format data export feature. The Raspberry Pi was configured to automatically initiate the packet logger software upon powering on and obtaining the correct time via the Internet.
