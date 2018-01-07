from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
# Create your views here.


def postWall(request):
    return render(request, 'postWall.html')


def newPost(request):
    print(request.POST)
    print(request.FILES)
    if request.user.is_authenticated:
        if request.method == 'POST':
            pic = request.FILES['pic']
            newPo = Post(userID=request.user.get_username(), photo=request.FILES['pic'], upWear=request.POST['upwear'], downWear=request.POST['downwear'],
                         shoes=request.POST['shoes'], accessories=request.POST['accessories'], weather=request.POST['weather'], temp=int(request.POST['temp']),iconClass=request.POST['weather-icon'])
            pic.name = str(newPo.postID) + '.jpg'
            newPo.photo = pic
            newPo.save()
    else:
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/index')
