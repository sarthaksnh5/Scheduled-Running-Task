import json
import os
from time import sleep
import requests
import csv
import datetime
import wget
import pyautogui
from subprocess import check_output, CalledProcessError, STDOUT

fieldName = ['looping', 'endTime', 'startTime', 'file', 'order']

mainUrl = 'http://192.168.5.113:8000/'
getUrl = mainUrl + 'getData'
writerArr = []
readerArr = []
executionArr = []
baseDirectory = os.getcwd() + '/download/'
first = 0
change = 0
videoDur = 0
noFiles = False


def maximizeFile(filetype):
    if filetype == 'jpg' or filetype == 'png' or filetype == 'jpeg':
        pyautogui.keyDown("alt")
        pyautogui.press("F11")
        pyautogui.keyUp("alt")
    elif filetype == 'pdf':
        pyautogui.press("F12")    


def closeFile():
    pyautogui.keyDown("alt")
    pyautogui.press("F4")
    pyautogui.keyUp("alt")


def getData():
    print("[STATUS] Program Started")
    print("[STATUS] Making Request")
    connect = requests.get(getUrl)
    print("[STATUS] Data Received")
    data = json.loads(connect.text)
    result = data['result']
    if result:
        messages = data['message']
        for message in messages:
            writerArr.append(message)
    else:
        print('[ERROR] ' + data)    


def writeInFile():    
    print("[STATUS] Writing in file")
    with open('data.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldName)
        writer.writerows(writerArr)


def readFileandStore():
    print("[STATUS] Readign from file")    
    with open('data.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)

        for row in reader:
            readerArr.append(row)


def downloadFiles():
    print("[STATUS] Downloading Files")
    if len(readerArr) > 0:
        for row in readerArr:
            start = row[2]
            end = row[1]
            start = datetime.datetime.strptime(start, '%H:%M:%S')
            end = datetime.datetime.strptime(end, '%H:%M:%S')
            timeDirectory = baseDirectory + '/' + \
                str(start.time()) + '-' + str(end.time()) + '/'
            url = mainUrl + 'media/' + str(row[3])
            filename = str(row[3])
            try:
                os.makedirs(timeDirectory)
            except Exception as e:
                yes = True

            try:
                fileDir = timeDirectory + filename
                if not os.path.exists(fileDir):
                    print('[STATUS] Downloading File ' + filename)
                    filename = wget.download(url, out=timeDirectory)                
            except Exception as e:
                print(e)


normal = True


def executeFile():
    print('[STATUS] starting file')
    now = datetime.datetime.now().time()
    global first
    global change
    global executionArr
    tempArr = []
    if first == 0:
        for row in readerArr:
            start = datetime.datetime.strptime(row[2], '%H:%M:%S').time()
            end = datetime.datetime.strptime(row[1], '%H:%M:%S').time()
            if now > start:
                if now < end:
                    filename = str(row[3])
                    directory = str(start) + '-' + str(end) + '/' + filename
                    executionArr.append((directory, row[4]))
        first = 1
    else:
        for row in readerArr:
            start = datetime.datetime.strptime(row[2], '%H:%M:%S').time()
            end = datetime.datetime.strptime(row[1], '%H:%M:%S').time()
            if now > start:
                if now < end:
                    filename = str(row[3])
                    directory = str(start) + '-' + str(end) + '/' + filename
                    tempArr.append((directory, row[4]))
        first = 2

    if first == 1:
        change = 1
    if first == 2:
        if executionArr != tempArr:
            executionArr = tempArr
            change = 1
        else:
            change = 0


pos = 0
next = False

def openFile():
    global pos
    global change
    global normal
    global next
    global videoDur
    if len(executionArr) > 0:        
        filetype = str(executionArr[pos][0]).split('.')[-1]
        filename = str(os.getcwd()) + '/download/' + executionArr[pos][0]
        
        if filetype == 'jpg' or filetype == 'png' or filetype == 'pdf' or filetype == 'jpeg':
            normal = True
        else:
            duration = getVideoLength(filename)
            videoDur = int(float(duration)) + 2                        
            normal = False

        if change == 1 or next:
            print('Opening file: ', filename)
            directory = 'xdg-open ' + \
                str(os.getcwd()) + '/download/' + executionArr[pos][0]
            closeFile()
            os.system(directory)
            sleep(2)
            maximizeFile(filetype)
            change = 0
            next = False

        if len(executionArr) > 1:
            if pos < len(executionArr) - 1:
                pos += 1
                next = True                
            else:
                pos = 0
                next = False
                     

    else:
        closeFile()
        directory = 'xdg-open ' + \
                str(os.getcwd()) + 'logo.png'
        os.system(directory)
        sleep(2)
        maximizeFile()
        writerArr = []
        readerArr = []
        getData()
        writeInFile()
        readFileandStore()
        downloadFiles()
        print('[STATUS] No files present')


def getVideoLength(video):
    command = ["ffprobe", "-v", "error", "-show_entries",
               "format=duration", "-of",
               "default=noprint_wrappers=1:nokey=1", video]

    try:
        output = check_output(command, stderr=STDOUT).decode()
    except CalledProcessError as e:
        output = e.output.decode()

    return output


def execute2(delay):

    while True:
        executeFile()
        openFile()
        if normal:
            sleep(delay)
        else:
            sleep(videoDur)


# try:

#     getData()
#     writeInFile()
#     readFileandStore()
#     downloadFiles()
#     execute2(5)

# except Exception as e:
#     print(e)

getData()
writeInFile()
readFileandStore()
downloadFiles()
execute2(5)
