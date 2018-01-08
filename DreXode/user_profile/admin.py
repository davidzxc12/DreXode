from django.contrib import admin
from .models import MyPhoto
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.


class PhotoInline(admin.StackedInline):
    model = MyPhoto
    can_delete = False
    verbose_name_plural = 'photo'

class UserAdmin(BaseUserAdmin):
    inlines = (PhotoInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
