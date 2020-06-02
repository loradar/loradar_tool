# Outputting LoRaWAN data as PCAP
## Description
This uses LoRa packet forwarder to forward the LoRa packets to a localhost with port 1700. Once packet forwarder is running, another process executes tcpdump that captures a loopback interface and outputs it as a pcap file. Afterwarads, we remove the Ethernet, IP and UDP headers (14+20+8) of the pcap file and set linktype to user (147). Finally, the edited pcap file is loaded to Wireshark, where the protocol is changed to LoRaWAN.

## Instructions
* Users should flash the correct configuration of LoRadar on the microSD card
` sudo apt-get update -y
sudo apt-get install -y bittwist
sudo apt-get install -y tcpdump

sudo tcpdump -s 0 -AUq port 1700 -w trial.pcap
bittwiste -I trial.pcap -O dump_dlt_user.pcap -M 147 -D 1-42`
