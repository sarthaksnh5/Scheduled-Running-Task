from datetime import *
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Q

from base.models import FileData, FileModel

# Create your views here.

data = {'message': '', 'result': False}

def loginUser(request):
    if request.method == "POST":
        print('POST')
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, 'Username or Password is wrong')        

    return render(request, 'base/login.html')

@login_required('')
def index(request):
    files = FileModel.objects.all()
    fileData = FileData.objects.all()

    context = {
        'files': files,
        'filesData': fileData
    }
    return render(request, 'base/data.html', context=context)

def getFile(request):
    try:
        requestedTime = datetime.time(datetime.now())
        files = FileModel.objects.filter(Q(startTime__lte=F('endTime')), Q(startTime__lte=requestedTime), endTime__gte=requestedTime)
        completeData = []
        for file in files:
            filesData = FileData.objects.filter(fileModel=file)            
            for fileData in filesData:
                temp = {                    
                    'looping': file.looping,
                    'endTime': file.endTime,
                    'startTime': file.startTime,
                    'file': str(fileData.file),
                    'time': fileData.time
                }
                completeData.append(temp)

        data['message'] = completeData
        data['result'] = True
    except Exception as e:
        data['message'] = str(e)
        data['result'] = False
    

    return JsonResponse(data)
    
@login_required('')
def changeSchedule(request):
    return render(request, 'base/index.html')

def deleteEntry(request, id):    
    instance = FileModel.objects.get(id=id)        
    if instance != None:
        FileData.objects.filter(fileModel=instance).delete()
        instance.delete()
        return redirect('base')

@login_required('')
def addFiles(request):
    if request.method == 'POST':
        try:                        
            FileData.objects.all().delete()
            FileModel.objects.all().delete()
            entryCount= request.POST['count']            
            for i in range(int(entryCount)):                
                fileCount = request.POST['fileCount_'+str(i)]
                if fileCount == '1':
                    startTime = request.POST['startTime_0_'+str(i)]
                    endTime = request.POST['endTime_0_'+str(i)]
                    looping = request.POST['looping_0_'+str(i)]
                    file = request.FILES['file_0_'+str(i)]
                    modelInstance = FileModel(fileCount=fileCount, looping=looping, endTime=endTime, startTime=startTime)
                    modelInstance.save()                    
                    FileData(fileModel=modelInstance, file=file, time=0).save()
                else:
                    startTime = request.POST['startTime_0_'+str(i)]
                    endTime = request.POST['endTime_0_'+str(i)]
                    looping = request.POST['looping_0_'+str(i)]
                    modelInstance = FileModel(fileCount=fileCount, looping=looping, endTime=endTime, startTime=startTime)
                    modelInstance.save()                
                    for j in range(int(fileCount)):                    
                        file = request.FILES['file_'+str(j)+'_'+str(i)]
                        order = request.POST['time_'+str(j)+'_'+str(i)]
                        FileData(fileModel=modelInstance, file=file, time=order).save()        

            data['message'] = 1
            data['result'] = True
        except Exception as e:
            FileData.objects.all().delete()
            FileModel.objects.all().delete()
            data['message'] = str(e)
            print(e)
            data['result'] = False


        return JsonResponse(data)

def logoutUser(request):
    logout(request)
    return redirect('home')
