from django.shortcuts import render,redirect
from django.contrib.auth import logout as auth_logout,login as auth_login
from django.contrib.auth.models import User
from .forms import SignupForm,LoginForm
from .models import ProfilePic

# Create your views here.

def Signup(req):
    if req.user:
        return redirect('/')

    if req.method == 'POST':
        form = SignupForm(req.POST,req.FILES)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            re_password = form.cleaned_data['re_password']
            profile_pic = form.cleaned_data['profile_pic']

            db_username = User.objects.filter(username = username).values()
            db_email = User.objects.filter(email = email).values()

            if not db_username and not db_email and password == re_password:
                user = User.objects.create_user(username = username, email = email, password = password)
                ProfilePic.objects.create(user_id = user.id,file = profile_pic)

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
    if req.user:
        return redirect('/')

    global next_url
    
    if req.method == 'GET':
        if req.GET.get('next'):
            next_url = req.GET.get('next')
        else:
            next_url = None

    if req.method == 'POST':
        form = LoginForm(req.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate_user(username_or_email, password)

            if user is not None:
                auth_login(req, user)

                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/')
            else:
                error = 'Username / Email or password is invalid'
                return render(req,'Login.html',{"error":error})
        else:
            error = 'Something went wrong try again'
            return render(req,'Login.html',{"error":error})
  
    else:
        return render(req,'Login.html')


def Logout(req):
    auth_logout(req)
    return redirect('/login')


def authenticate_user (username_or_email, password):
    user = User.objects.filter(email=username_or_email).first()

    if not user:
        user = User.objects.filter(username=username_or_email).first()
    
    if user and user.check_password(password) and user.is_active:
        return user

    return None