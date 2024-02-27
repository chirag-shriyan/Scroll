from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url = '/login')
def index(req):
    return render(req,'index.html')