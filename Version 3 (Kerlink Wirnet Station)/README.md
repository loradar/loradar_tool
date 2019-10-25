Follow these steps to perform passive packet sniffing using Kerlink Wirnet Station

1.	Connect Kerlink Wirnet Station to ethernet interface of Raspberry Pi.
2.	Open chromium browser from Raspberry Pi.
3.	Go to the IP address of Kerlink gateway.  
	•If you are using a static IP address, it should be 192.168.13.151
4.	Login to the gateway using your username and password.
5.	Run “Downloader.py” to collect log data from Kerlink gateway without closing the chromium browser.
6.	Copy “LogReader.py” to downloads folder and run.
7.	A new file called “Packets.cvs” will be created with sniffed packets.

If you are having difficulties in step 3, please follow these steps to connect to Kerlink Wirnet Station

1.	Please make sure that the wiring of the  Kerlink Wirnet Station is okay.
2.	For the Power over Ethernet injector  
	•Connect “Data & Power out”   to the cable connected to the gateway.  
	•Data In : Cable connected to the network (router).
3.	Gain access to the router and see whether that the gateway has obtained an IP-address from it. (It should and that is used to connect to the gate-way)
4.	From a browser try to connect to that IP-Address.
5.	Enter your login details, these are the default username and password:   
	•Login : admin  
	•Password: spnpwd
6.	If it does not obtain an IP from the router, connect the cable that connected to the router to the computer and try following,  
	•Try to connect to the IP 192.168.13.151. Please set the computers LAN to the same (something like 192.168.13.150).
