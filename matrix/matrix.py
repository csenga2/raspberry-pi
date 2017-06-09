import serial
import datetime
import time
import requests
import bs4
import threading

endChar="="
newLine="\n"
currentTemp="NA"
url="https://www.idokep.hu/idojaras/Budapest"

def idokepCrawl():
    global currentTemp
    while True:
        try:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text,"html5lib")
            currentTempDiv=soup.find("div",{"class":"homerseklet"})
            currentTemp=''.join(map(str, currentTempDiv.contents))
            currentTemp=currentTemp.replace('°','\'')
            time.sleep(60*5)
        except:
            pass

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
    text=getCurrentDate()+' '+getCurrentTime()+newLine+currentTemp+endChar
    serialPort.write(text.encode())
    serialPort.flushOutput()
    time.sleep(10)

serialPort.close()



    
    
