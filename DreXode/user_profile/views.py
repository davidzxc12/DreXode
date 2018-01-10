import django
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from user_profile.models import MyPhoto, FollowRelation
from user_profile.forms import UploadPhotoForm
from el_pagination.decorators import page_template
from posts.models import Post

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect('/index')
                # Redirect to a success page.

        else:
            request.session['login_err'] = '使用者帳號或密碼有誤'
            return HttpResponseRedirect('/login')
            # Return an 'invalid login' error message.
    else:
        if('login_err' in request.session and request.session['login_err'] != ''):
            err_msg = request.session['login_err']
            request.session['login_err'] = ''
            return render(request, 'login.html', {'action': 'login', 'error_message': err_msg})
        return render(request, 'login.html', {'action': 'login'})


def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect('/login')


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    if(request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPW = request.POST['repeatpassword']
        if(repeatPW != password):
            request.session['login_err'] = '兩次密碼輸入不同'
            return HttpResponseRedirect('/register')
        if(User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            request.session['login_err'] = '使用者名稱或Email已被使用'
            return HttpResponseRedirect('/register')
        user = User.objects.create_user(username, email, password)
        user.save()
        user = authenticate(username=username, password=password)
        django.contrib.auth.login(request, user)
        return HttpResponseRedirect('/index')
    else:
        if('login_err' in request.session and request.session['login_err'] != ''):
            err_msg = request.session['login_err']
            request.session['login_err'] = ''
            return render(request, 'login.html', {'action': 'register', 'error_message': err_msg})
        return render(request, 'login.html', {'action': 'register'})


@page_template('post_template.html')
def profile(request, pk, template='profile.html', extra_context=None):
    if request.method == 'POST':
        action = request.POST['profile_action']
        if action == 'photo' and authed == True:
            form = UploadPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                pic = request.FILES['photo']
                pic.name = str(request.user) + '.jpg'
                user = request.user
                user.myprofile.photo = pic
                user.save()
                return HttpResponseRedirect("/profile/" + pk)

    # render page
    authed = False
    if request.user.username == pk:
        authed = True
    userObj = User.objects.get(username=pk)

    photo_path = ''
    if bool(User.objects.get(username=pk).myprofile.photo):
        photo_path = User.objects.get(username=pk).myprofile.photo.url
    f = UploadPhotoForm()
    follows = FollowRelation.objects.filter(follower=userObj)
    print(follows)
    context = {'photo_path': photo_path, 'f': f, 'entry_list': Post.objects.filter(
        userID=userObj).order_by('-createTime'), 'authed': authed,'pk':pk,'follows':follows}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def ajaxFollow(request):
    if request.is_ajax() and request.method == 'POST':
        followerID = request.POST['follower']
        followingID = request.POST['following']
        action = True if request.POST['action'] == 'follow' else False
        followerObj = User.objects.get(username=followerID)
        followingObj = User.objects.get(username=followingID)
        if(action):
            FollowRelation.objects.get_or_create(
                follower=followerObj,
                following=followingObj,
                defaults={'follower': followerObj,
                        'following': followingObj}
            )
        else:
            FollowRelation.objects.filter(follower=followerObj,following=followingObj).delete()
        return JsonResponse({'isSuccess':True})
