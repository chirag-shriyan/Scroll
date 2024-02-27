from django.shortcuts import render,redirect
from django.contrib.auth import logout as auth_logout,login as auth_login ,authenticate
from django.contrib.auth.models import User
from .forms import SignupForm,LoginForm

# Create your views here.

def Signup(req):

    if req.method == 'POST':
        form = SignupForm(req.POST)

        if form.is_valid():
            username = req.POST['username']
            email = req.POST['email']
            password = req.POST['password']
            re_password = req.POST['re_password']

            db_username = User.objects.filter(username = username).values()
            db_email = User.objects.filter(email = email).values()

            if not db_username and not db_email and password == re_password:
                user = User.objects.create_user(username = username, email = email, password = password)
                user.save()
                return redirect('/login')
            elif password != re_password:
                error = 'Password and confirm password should be the same'
                return render(req,'Signup.html',{"error":error})
            elif db_username:
                error = 'Username already exist'
                return render(req,'Signup.html',{"error":error})
            elif db_email:
                error = 'Email already exist'
                return render(req,'Signup.html',{"error":error})
        
                
        else:
            error = 'Something went wrong try again'
            return render(req,'Signup.html',{"error":error})
        
    else:
        return render(req,'Signup.html')


def Login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)

        if form.is_valid():
            username = req.POST['username']
            password = req.POST['password']
            user = authenticate(req, username = username, password = password)

            if user is not None:
                auth_login(req, user)
                return redirect('/')
            else:
                error = 'Username or password is invalid'
                return render(req,'Login.html',{"error":error})
        else:
            error = 'Something went wrong try again'
            return render(req,'Login.html.html',{"error":error})
  
    else:
        return render(req,'Login.html')


def Logout(req):
    auth_logout(req)
    return redirect('/login')