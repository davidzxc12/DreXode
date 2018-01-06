from django.shortcuts import render

# Create your views here.

def news_feed(request):
    return render(request,'news_feed.html')