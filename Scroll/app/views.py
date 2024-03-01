from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from myauth.models import ProfilePic

# Create your views here.

@login_required(login_url = '/login')
def index(req):
   
    username = str(req.user).capitalize()
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    DATA = Post.objects.filter(is_public = True).order_by('-updated_at').values()

    for user in DATA:
        added_by = str(User.objects.get(id = user['user_id'])).capitalize()
        added_by_profile = ProfilePic.objects.filter(user_id = user['user_id']).values().first()

        if added_by_profile:
            user['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
        else:
            user['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}
        
        user['added_by'] = added_by

    context = {
        "username" : username,
        "profile_pic" : profile_pic,
        "data" : DATA
    }
    return render(req,'index.html',context)
   