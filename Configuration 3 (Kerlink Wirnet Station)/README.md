# _LoRadar_ (Configuration 3)

## Hardware used
This configuration setup uses the following hardware:
- **Single board computer:** Raspberry Pi 3
- **LoRa module:** Kerlink Wirnet Station, a commercial bidirectional gateway
- **Antenna:** A fibreglass 1/2 wave 860-960 MHz antenna with 6 dBi gain attached to the LoRa module
- **Connection bridge:** Ethernet cable to of the gateway was connected to Raspberry Pi 3 via power injector
- **Storage:** 32 GB microSD card inserted to the Raspberry Pi for data storage

## Instructions
**Follow these steps to perform passive packet sniffing using Kerlink Wirnet Station**

1) Connect Kerlink Wirnet Station to ethernet interface of Raspberry Pi
2) Open chromium browser from Raspberry Pi
3) Go to the IP address of Kerlink gateway  
	• If you are using a static IP address, it should be 192.168.13.151
4) Login to the gateway using your username and password
5) Run “Downloader.py” to collect log data from Kerlink gateway without closing the chromium browser
6) Copy “LogReader.py” to downloads folder and run
7) A new file called “Packets.cvs” will be created with sniffed packets

**If you are having difficulties in step 3, please follow these steps to connect to Kerlink Wirnet Station**

1) Please make sure that the wiring of the  Kerlink Wirnet Station is okay  
2) For the Power over Ethernet injector  
	• Connect “Data & Power out”   to the cable connected to the gateway  
	• Data In : Cable connected to the network (router)
3) Gain access to the router and see whether that the gateway has obtained an IP-address from it. (It should and that is used to connect to the gate-way)
4) From a browser try to connect to that IP-Address
5) Enter your login details, these are the default username and password:   
	• Login : admin  
	• Password: spnpwd
6) If it does not obtain an IP from the router, connect the cable that connected to the router to the computer and try the following:    
	• Try to connect to the IP 192.168.13.151. Please set the computers LAN to the same (something like 192.168.13.150)

## Information extraction (Requires Internet Connection)
To extract the information, follow the steps below:
1) Download the _Config3\_LoRadar\_Extractor.py_ python script from above and place it in the _Downloads_ folder of the Raspberry Pi
2) Open a terminal and enter run the following commands to install the required libraries:  
`sudo apt-get install python3-matplotlib --assume-yes`  
`sudo apt-get install python3-pandas --assume-yes`
3) Open the python script with _Python 3 (IDLE)_
4) Run the module (Requires Internet Connection)
5) Upon successful extraction, a csv file will be created in the same directory as the _Config3\_LoRadar\_Extractor.py_ python script
