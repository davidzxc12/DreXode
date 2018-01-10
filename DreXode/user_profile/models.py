from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.


class OverwriteStorage(FileSystemStorage):
    '''
    Muda o comportamento padrão do Django e o faz sobrescrever arquivos de
    mesmo nome que foram carregados pelo usuário ao invés de renomeá-los.
    '''

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class FollowRelation(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follower")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")



class MyPhoto(models.Model):
    userID = models.OneToOneField(
        User, related_name='myprofile', on_delete=models.CASCADE)
    photo = models.FileField(upload_to='myPhoto', storage=OverwriteStorage())


@receiver(post_save, sender=User)
def create_user_photo(sender, instance, created, **kwargs):
    if created:
        MyPhoto.objects.create(userID=instance)


@receiver(post_save, sender=User)
def save_user_photo(sender, instance, **kwargs):
    instance.myprofile.save()
