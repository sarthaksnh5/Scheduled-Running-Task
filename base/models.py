import os
from django.db import models

# Create your models here.

class FileModel(models.Model):
    fileCount = models.CharField(max_length=200)
    looping = models.CharField(max_length=3, default=1)
    startTime = models.TimeField()
    endTime = models.TimeField()    
    date = models.DateTimeField(auto_now=True)
    
class FileData(models.Model):
    fileModel = models.ForeignKey(FileModel, on_delete=models.PROTECT)    
    date = models.DateTimeField(auto_now=True)
    file = models.FileField()
    time = models.CharField(max_length=2, default=1)

    def filename(self):
        return os.path.basename(self.file.name)