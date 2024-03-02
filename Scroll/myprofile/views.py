from django.shortcuts import render
from django.contrib.auth.models import User
from myauth.models import ProfilePic
from posts.models import Post
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url = '/login')
def Search(req):

    search = req.GET.get('q')
    if search:
        DATA = User.objects.filter(Q(username__contains = search) & ~Q(id = req.user.id)).values()
        not_found = False

        if len(DATA) > 0:
            for user in DATA:
                profile_pic = ProfilePic.objects.filter(user_id = user['id']).values().first()
                
                if profile_pic:
                    user['profile_pic'] = {"file": profile_pic['file'] , "exist": True}
                else:
                    user['profile_pic'] = {"file": 'images/profile.jpg', "exist": False}
        else:
            not_found = True

        context = {
            "data": DATA,
            "not_found": not_found
        }

        return render(req,'search.html',context)

    return render(req,'search.html')

@login_required(login_url = '/login')
def User_Profile(req):

    username = req.user.username.capitalize()
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()
    not_found = False

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    DATA = Post.objects.filter(user_id = req.user.id).values()

    if not len(DATA) > 0:
        not_found = True

    context = {
        "username": username,
        "profile_pic": profile_pic,
        "data": DATA,
        "not_found": not_found
    }

    if req.method == 'POST':

        return render(req,'user_profile.html',context)
    else:
        return render(req,'user_profile.html',context)