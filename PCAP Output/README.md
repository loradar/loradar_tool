# Outputting LoRaWAN data as PCAP
## Description
This uses LoRa packet forwarder to forward the LoRa packets to a localhost with port 1700. Once packet forwarder is running, another process executes tcpdump that captures a loopback interface and outputs it as a pcap file. Afterwarads, we remove the Ethernet, IP and UDP headers (14+20+8) of the pcap file and set linktype to user (147). Finally, the edited pcap file is loaded to Wireshark, where the protocol is changed to LoRaWAN.

## Instructions
1. Users should first flash the correct configuration of LoRadar on the microSD card.

2. Clone the `local_packet_forwader` directory to the Raspberry Pi.

3. Install the following dependencies.
    ```
    sudo apt-get update -y
    sudo apt-get install -y bittwist
    sudo apt-get install -y tcpdump
    sudo apt-get install -y screen
    ```
    
4. Create a screen session.
    ```
    screen
    ```
    
5. Within this screen session, `cd` to the 'local_packet_forwarder' directory within Raspberry Pi. Execute the following to start capturing packets on port 1700 and outputting it as `capture.pcap`:
    ```
    cd lora_pkt_fwd/
    sudo tcpdump -s 0 -AUq port 1700 -w capture.pcap
    ```
    
6. Detach from the screen by pressing `ctrl + a + d` on the keyboard.

7. Start a new screen session by typing `screen` in the terminal.

8. `cd` to the 'local_packet_forwarder' directory within Raspberry Pi. Execute the following to start forwarding packets to localhost:
    ```
    cd lora_pkt_fwd/
    sudo chmod +x lora_pkt_fwd
    sudo ./lora_pkt_fwd
    ```
    
9. To terminate the packet forwarder session, press `ctrl + c` on the keyboard and type `exit` in the terminal to end the screen session.

10. Navigate to the other screen by typing `screen -r -d` in the terminal.

11. End the packet capture session by pressing `ctrl + c` on the keyboard. You will now see a new `capture.pcap` file created in the directory.

12. Process the .pcap data to remove the unnecessary Ethernet, IP and UDP headers (14+20+8) of the pcap file and set linktype to user (147). This process will intake the `capture.pcap` file and output it as `processed_capture.pcap`.
    ```
    bittwiste -I capture.pcap -O dump_dlt_user.pcap -M 147 -D 1-42
    ```
    
13. Open the `processed_capture.pcap` file in Wireshark.

14. Navigate to `Edit -> Preferences -> Protocols -> DLT_USER -> Edit...`.

15. Input `lorawan` as the Payload protocol, `14` as the header size, then click OK.

16. You will now see LoRaWAN fields under the frame information.
