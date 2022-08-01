import time
import pyautogui
import os
import wget
from subprocess import check_output, CalledProcessError, STDOUT

timeDirectory = os.getcwd() + '/download/'

mainUrl = 'http://192.168.1.9:8000/'

def closeFile():
    pyautogui.keyDown("alt")
    pyautogui.press("F4")
    pyautogui.keyUp("alt")


def maximizeFile(filetype):
    if filetype == 'jpg' or filetype == 'png' or filetype == 'jpeg':
        pyautogui.keyDown("alt")
        pyautogui.press("F11")
        pyautogui.keyUp("alt")
    elif filetype == 'pdf':
        pyautogui.press("F12")

def openFile(file, delay = 0):
    filetype = str(file).split('.')[-1]
    filePath = timeDirectory + str(file)
    directory = 'xdg-open ' + \
                str(os.getcwd()) + '/download/' + str(file)
    closeFile()
    os.system(directory)
    time.sleep(2)
    maximizeFile(filetype)

    if filetype == 'jpg' or filetype == 'png' or filetype == 'pdf' or filetype == 'jpeg':        
        time.sleep(delay)
        closeFile()
    else:
        duration = getVideoLength(filePath)
        videoDur = int(float(duration)) + 2
        time.sleep(videoDur)
        closeFile()

def downloadFile(url):
    
    url = mainUrl + 'media/' + str(url)
    filename = str(url)
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

def getVideoLength(video):
    command = ["ffprobe", "-v", "error", "-show_entries",
               "format=duration", "-of",
               "default=noprint_wrappers=1:nokey=1", video]

    try:
        output = check_output(command, stderr=STDOUT).decode()
    except CalledProcessError as e:
        output = e.output.decode()

    return output