from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from el_pagination.decorators import page_template
from .models import Post, Comment, Like
from django.contrib.auth.models import User
from django.db.models import Q
from user_profile.models import FollowRelation
from operator import ior
from functools import reduce



# Create your views here.

@page_template('post_template.html')
def postWall(request, template='postWall.html', extra_context=None):
    context = {'entry_list': Post.objects.all().order_by('-createTime'), }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


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
    return render(request, 'index.html')


@page_template('comment_template.html')
def postView(request, pk, template='post.html', extra_context=None):
    entry = Post.objects.get(postID=pk)
    context = {'entry_list': Comment.objects.filter(
        postID=entry).order_by('-createTime'), 'entry': entry}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def newComment(request, pk):
    if(request.method == 'POST'):
        comment = request.POST['comment']
        postObj = Post.objects.get(postID=pk)
        commentObj = Comment(userID=request.user,
                             comment=comment, postID=postObj)
        commentObj.save()
        return HttpResponseRedirect('/post/' + pk)

    else:
        return HttpResponseRedirect('/post/' + pk)


def ajaxAddLike(request):
    if request.is_ajax() and request.method == 'POST':
        userID = request.POST['user']
        postID = request.POST['post']
        print(userID)
        action = True if request.POST['action'] == 'like' else False
        userObj = User.objects.get(username=userID)
        postObj = Post.objects.get(postID=postID)
        Like.objects.update_or_create(userID=userObj, postID=postObj, defaults={
                                      'userID': userObj, 'postID': postObj, 'like': action})
        count = Like.objects.filter(postID=postObj,like=action).count()
        return JsonResponse({'count':count})


@page_template('post_template.html')
def filterPostWall(request,action,template='postWall.html',extra_context=None):
    weatherCondition=['Thunderstorm','Drizzle','Rain','Snow','Atmosphere','Clear','Clouds','Extreme','Additional']
    if action=='top':
        context = {'entry_list': sorted(Post.objects.all(),key=lambda t:t.count_like(),reverse=True)}
    elif action=='following':
        qCondition = []
        Ufollow = FollowRelation.objects.filter(follower=request.user)
        for U in Ufollow:
            qCondition.append(Q(userID=U.following))
        if len(qCondition)>0:
            context = {'entry_list': Post.objects.filter(reduce(ior, qCondition)).order_by('-createTime')}
        else:
            context = {'entry_list': []}
    elif action == 'newest':
        context = {'entry_list': Post.objects.all().order_by('-createTime')}
    elif action in weatherCondition:
        context = {'entry_list': Post.objects.filter(weather=action).order_by('-createTime')}
    else:
        return HttpResponseRedirect('/feed')

    context.update({'action':action})
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)
    
