import serial
import datetime
import time
import requests
import bs4
import threading

import sys
import Adafruit_DHT as dht
reload(sys)
sys.setdefaultencoding('utf8')

endChar="="
newLine="\n"
currentTemp="NA"
url="https://www.idokep.hu/idojaras/Budapest"

def idokepCrawl():
    global currentTemp
    while True:
        try:
            response = requests.get(url)
            asciiFilteredText=response.text.encode('ascii',errors='ignore')
            soup = bs4.BeautifulSoup(asciiFilteredText,from_encoding="utf-8")
            currentTempDiv=soup.find("div",{"class":"homerseklet"})
            currentTemp=''+currentTempDiv.contents[0]
            currentTemp=currentTemp.decode('utf-8').encode('utf-8').replace('°','').replace('C','')
            time.sleep(60*5)
        except Exception as e:
            print 'My exception occurred, value:', e
            currentTemp="ERR"

def getCurrentTime():
    return time.strftime("%H:%M", time.localtime())

def getCurrentDate():
    return time.strftime("%Y.%m.%d", time.localtime())

serialPort = serial.Serial("/dev/ttyACM0",115200)
serialPort.flushInput()
serialPort.flushOutput()

idokepThread=threading.Thread(name="idokep",target=idokepCrawl)
idokepThread.start()

while True:
    h,t = dht.read_retry(dht.DHT22, 4)
    text=getCurrentDate()+' '+getCurrentTime()+newLine+'T:'+currentTemp+'|'+str(int(round(t)))+'\'C H:'+ str(int(round(h)))+'%'+endChar
    serialPort.write(text.encode())
    serialPort.flushOutput()
    time.sleep(10)

serialPort.close()



    
    
