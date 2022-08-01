import json
from multiprocessing import Process, Queue
import time
import requests

from filefunctions import downloadFile, openFile

mainUrl = 'http://192.168.1.9:8000/'
dataUrl = mainUrl + 'getData'
first = 0
initial = []
change = 0

def getData(q):    
    try:
        global first, initial, change 
        while True:
            connect = requests.get(dataUrl)
            data = json.loads(connect.text)                               
            if data['result']:                                         
                if first == 0:
                    initial = data['message']
                    first = 1
                    change = 1
                else:
                    if data['message'] == initial:
                        change = 0
                    else:
                        initial = data['message']
                        change = 1
            
            if change == 1:
                q.put({'data': initial})
            else:
                print('No Change')
                time.sleep(1)

    except Exception as e:
        print(e)                  

def serializerData(q):    
    try:
        while True:
            initial = q.get()['data']
            for file in initial:
                fileUrl = file['file']
                downloadFile(fileUrl)
                openFile(fileUrl, file['time'])
    except Exception as e:
        print(e)

q = Queue

if __name__ == "__main__":
    p1 = Process(target=getData, args=(q, ))
    p2 = Process(target=serializerData, args=(q, ))
    p1.start()
    p2.start()
    p1.join()
    p2.join()