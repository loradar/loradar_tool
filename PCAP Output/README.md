# Outputting LoRaWAN data as PCAP
## Description
This uses LoRa packet forwarder to forward the LoRa packets to a localhost with port 1700. Once packet forwarder is running, another process executes tcpdump that captures a loopback interface and outputs it as a pcap file. Afterwarads, we remove the Ethernet, IP and UDP headers (14+20+8) of the pcap file and set linktype to user (147). Finally, the edited pcap file is loaded to Wireshark, where the protocol is changed to LoRaWAN.

## Instructions
* Users should flash the correct configuration of LoRadar on the microSD card
