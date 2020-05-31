# Description on the Global Configuration File

## Specifing channels
Eight channels can be configured to receive LoRa packets using 125 kHz bandwith. These channels are configured in the **chan_multiSF_x** settings. Each channel has an enable boolean, a selected radio and an intermediate frequency. The channel frequency will freq setting of the radio plus the 'if' setting of the channel.
* enable: true if this channel is enabled for use
* radio: selected radio to listen for packets
* if: intermediate frequency offset applied to the selected radio “freq” setting

Two additional channels can be configured with the chan_Lora_std and chan_FSK settings
* enable: true if this channel is enabled for use
* radio: selected radio to listen for packets
* if: intermediate frequency offset applied to the selected radio “freq” setting
* bandwidth: channel bandwidth
* spread_factor (LoRa): channel spreading factor (7-12)
* datarate (FSK): channel datarate in bps

## Other configurations
* gateway_ID: gateway identifier sent in each message to the network server
* server_address: address of the network server
* serv_port_up: port for sending uplink packets to the network server
* serv_port_down: port to ping network server and receive downlink packets
* keepalive_interval: interval to ping the network server
* stat_interval: interval to send stat messages to the network server
* push_timeout_ms: socket timeout when publishing messages to the network server
* autoquit_threshold: number of keepalive messages without response to wait before quitting Multi-Tech Systems, Inc.
* forward_crc_valid: enable to forward valid packets to the network server, default: true
* forward_crc_error: enable to forward CRC failed packets to the network server, default: true. The network server will reject packets with failed CRC, it may not be necessary to forward the packets except for a statistic of local RF quality or to monitor the gateway performance over time. Some random CRC failed packets are expected to be received from random noise.
* forward_crc_disabled: enable to forward packets without CRC enabled to the network server, default: false. LoRaWAN protocol expects uplink packets to have CRC enabled.
