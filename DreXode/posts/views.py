from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



def postWall(request):
    return render(request,'postWall.html')