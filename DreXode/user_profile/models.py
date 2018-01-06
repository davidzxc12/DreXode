from django.db import models

# Create your models here.


class Profile(models.Model):
    userID = models.CharField(max_length=100,blank=False, null=False)
    photo_url = models.URLField()


