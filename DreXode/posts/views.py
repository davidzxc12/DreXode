from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from el_pagination.decorators import page_template
from .models import Post


# Create your views here.

@page_template('post_template.html')
def postWall(request, template = 'postWall.html',extra_context=None):
    context = {'entry_list':Post.objects.all(),}
    if extra_context is not None:
        context.update(extra_context)
    return render(request,template,context)


def newPost(request):
    print(request.POST)
    print(request.FILES)
    if request.user.is_authenticated:
        if request.method == 'POST':
            pic = request.FILES['pic']
            newPo = Post(userID=request.user, photo=request.FILES['pic'], upWear=request.POST['upwear'], downWear=request.POST['downwear'],
                         shoes=request.POST['shoes'], accessories=request.POST['accessories'], weather=request.POST['weather'], temp=int(request.POST['temp']), iconClass=request.POST['weather-icon'])
            pic.name = str(newPo.postID) + '.jpg'
            newPo.photo = pic
            newPo.save()
    else:
        return HttpResponseRedirect('/login')
    return HttpResponseRedirect('/index')

def index(request):
    if request.user and request.user.is_authenticated:
        return HttpResponseRedirect('/feed')
    return render(request,'index.html')

def postView(request,pk):
    entry = Post.objects.get(postID=pk)
    return render(request,'post.html',locals())