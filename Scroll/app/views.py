from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url = '/login')
def index(req):
    username = str(req.user).capitalize()
    context = {
        "username" : username
    }
    return render(req,'index.html',context)