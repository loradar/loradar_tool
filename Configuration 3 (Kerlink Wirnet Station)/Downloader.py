#Please update 'IPAddress' to IP address of the Kerlink gateway

IPAddress='192.168.13.151'


#This python file will download log from kerlink gateway every 300 seconds
import webbrowser, os , sys ,time
urL='https://'+IPAddress+'/download_log.dhtml?type=0'
chrome_path="/usr/lib/chromium-browser/chromium-browser"
i=0
while (1):
    webbrowser.get(chrome_path).open_new_tab(urL)
    i=i+1
    print('new download '+str(i))
    time.sleep(300)
