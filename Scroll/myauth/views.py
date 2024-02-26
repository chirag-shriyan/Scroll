from django.shortcuts import render,redirect
from django.contrib.auth import logout as auth_logout,login as auth_login
from django.contrib.auth.models import User

# Create your views here.

def Signup(req):
    return render(req,'Signup.html')
    # auth_logout(request)
    # return redirect('/')

def Login(req):
    return render(req,'Login.html')
    # auth_logout(request)
    # return redirect('/')

def Logout(req):
    auth_logout(req)
    return redirect('/')
