from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post
from myauth.models import ProfilePic

# Create your views here.

@login_required(login_url = '/login')
def Index(req):
   
    username = str(req.user).capitalize()
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    POST_DATA = Post.objects.filter(is_public = True).order_by('-updated_at').values()

    for user in POST_DATA:
        added_by = str(User.objects.get(id = user['user_id'])).capitalize()
        added_by_url = '/users/' + User.objects.get(id = user['user_id']).username 
        added_by_profile = ProfilePic.objects.filter(user_id = user['user_id']).values().first()

        user['added_by'] = added_by
        user['added_by_url'] = added_by_url
        if added_by_profile:
            user['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
        else:
            user['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}
        
    SUGGESTIONS_DATA = User.objects.all().order_by('-date_joined')[:4].values()
    no_suggestions_data = False

    if not len(SUGGESTIONS_DATA) > 0:
        no_suggestions_data = True

    for user in SUGGESTIONS_DATA:
        added_by = user['username'].capitalize()
        added_by_profile = ProfilePic.objects.filter(user_id = user['id']).values().first()

        user['added_by'] = added_by
        if added_by_profile:
            user['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
        else:
            user['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

    context = {
        "username" : username,
        "profile_pic" : profile_pic,
        "post_data" : POST_DATA,
        "suggestions_data" : SUGGESTIONS_DATA,
        "no_suggestions_data" : no_suggestions_data
    }
    return render(req,'index.html',context)
   