from django.db import models
import uuid
import django.utils.timezone as timezone

from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    postID = models.UUIDField(unique=True,primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.FileField(upload_to='postPhoto')
    upWear = models.CharField(max_length=500)
    downWear = models.CharField(max_length=500)
    shoes = models.CharField(max_length=500)
    accessories = models.CharField(max_length=500)
    weather = models.CharField(max_length=100)
    temp = models.IntegerField()
    iconClass = models.CharField(max_length=100)
    createTime = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    postID = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    createTime = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    postID = models.ForeignKey(Post,on_delete=models.CASCADE)
    like = models.BooleanField()
