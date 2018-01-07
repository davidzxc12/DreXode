from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.


class OverwriteStorage(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    '''
    def get_available_name(self, name,max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class myPhoto(models.Model):
    userID = models.CharField(max_length=100,blank=False, null=False,unique=True)
    photo = models.FileField(upload_to='myPhoto',storage=OverwriteStorage())

    def __str__(self):
        return self.userID