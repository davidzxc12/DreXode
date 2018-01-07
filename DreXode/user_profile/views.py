import django
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect 
from user_profile.models import Profile

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
        if('login_err' in request.session and request.session['login_err']!=''):
            err_msg = request.session['login_err']
            request.session['login_err'] = ''
            return render(request, 'login.html',{'action':'login','error_message':err_msg})
        return render(request, 'login.html',{'action':'login'})

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect('/login')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index')
    if(request.method=='POST'):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPW = request.POST['repeatpassword']
        if(repeatPW != password):
            request.session['login_err'] = '兩次密碼輸入不同'
            return HttpResponseRedirect('/register')
        user = User.objects.create_user(username, email, password)
        user.save()
        Profile.objects.create(userID=username,photo_url='img/default_photo.png')
        user = authenticate(username=username, password=password)
        django.contrib.auth.login(request, user)
        return HttpResponseRedirect('/index')
    else:
        if('login_err' in request.session and request.session['login_err']!=''):
            err_msg = request.session['login_err']
            request.session['login_err'] = ''
            return render(request, 'login.html',{'action':'register','error_message':err_msg})
        return render(request, 'login.html',{'action':'register'})


def profile(request):
    if request.user.is_authenticated:
        userObj = Profile.objects.get(userID=request.user.get_username())
        return render(request,'profile.html',{'user':userObj})
    else:
        return HttpResponseRedirect('/login')