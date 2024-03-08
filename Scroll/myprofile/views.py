from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myauth.models import ProfilePic
from posts.models import Post
from .models import Follower


# Create your views here.

@login_required(login_url = '/login')
def Search(req):

    search = req.GET.get('q')
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}


    if search:
        DATA = User.objects.filter(Q(username__contains = search) & ~Q(id = req.user.id)).values().order_by('-date_joined')
        not_found = False

        if len(DATA) > 0:
            for user in DATA:
                user_profile_pic = ProfilePic.objects.filter(user_id = user['id']).values().first()
                
                if user_profile_pic:
                    user['profile_pic'] = {"file": user_profile_pic['file'] , "exist": True}
                else:
                    user['profile_pic'] = {"file": 'images/profile.jpg', "exist": False}
        else:
            not_found = True

        context = {
            "data": DATA,
            "not_found": not_found,
            "profile_pic": profile_pic,
        }

        return render(req,'search.html',context)

    return render(req,'search.html',{"profile_pic":profile_pic})

@login_required(login_url = '/login')
def My_Profile(req):

    username = req.user.username.capitalize()
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()
    num_of_followers = len(Follower.objects.filter(user_id = req.user.id).values())
    num_of_posts = len(Post.objects.filter(Q(user_id = req.user.id)).values())
    not_found = False

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    DATA = Post.objects.filter(user_id = req.user.id).values().order_by('-created_at')

    if not len(DATA) > 0:
        not_found = True

    context = {
        "username": username,
        "profile_pic": profile_pic,
        "data": DATA,
        "not_found": not_found,
        "num_of_followers":num_of_followers,
        "num_of_posts":num_of_posts
    }

    if req.method == 'POST':

        return render(req,'my_profile.html',context)
    else:
        return render(req,'my_profile.html',context)
    

def User_Profile(req,username = None):

    if username:
        
        USER_DATA = User.objects.filter(username = username).values()

        if len(USER_DATA) > 0:
            USER_DATA = USER_DATA[0]

            if USER_DATA['id'] != req.user.id:
                username = USER_DATA['username'].capitalize()
                profile_pic = ProfilePic.objects.filter(user_id = USER_DATA['id']).values().first()
                is_following = Follower.objects.filter(Q(user_id = USER_DATA['id']) & Q(follower_id = req.user.id)).first()
                num_of_followers = len(Follower.objects.filter(user_id = USER_DATA['id']).values())
                num_of_posts = len(Post.objects.filter(Q(user_id = USER_DATA['id']) & Q(is_public = True)).values())
                post_not_found = False
  
                if profile_pic:
                    profile_pic = {"file": profile_pic['file'] , "exist": True}
                else:
                    profile_pic = {"file": 'images/profile.jpg', "exist": False}

                POST_DATA = Post.objects.filter(Q(user_id = USER_DATA['id']) & Q(is_public = True)).values().order_by('-created_at')

                if not len(POST_DATA) > 0:
                    post_not_found = True

                context = {
                    "user_data": USER_DATA,
                    "post_data": POST_DATA,
                    "username": username,
                    "profile_pic": profile_pic,
                    "post_not_found": post_not_found,
                    "num_of_followers": num_of_followers,
                    "num_of_posts": num_of_posts,
                    "is_following":is_following
                }

                return render(req,'user_profile.html',context)
            else:
                return redirect('/profile')
        
        else:
            return render(req,'not_found.html')

    else:
        return render(req,'not_found.html')
    
import json
from django.http import JsonResponse
    
@login_required(login_url = '/login')  
def Handel_Follow_Req(req):
    if req.method == "POST":
        body = json.loads(req.body)
 
        is_following = Follower.objects.filter(Q(user_id = body['user_id']) & Q(follower_id = req.user.id)).first()

        if is_following == None:            
            Follower.objects.create(user_id = body['user_id'],follower_id = req.user.id)
            current_followers = len(Follower.objects.filter(user_id = body['user_id']).values())

            return JsonResponse({
                "status":200,
                "is_following":True,
                "current_followers": current_followers,
            })
        else:
            is_following.delete()
            current_followers = len(Follower.objects.filter(user_id = body['user_id']).values())

            return JsonResponse({
                "status":200,
                "is_following":False,
                "current_followers":current_followers,
            })
    return render(req,'not_found.html')

@login_required(login_url = '/login')  
def Handel_Edit_User(req):

    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    
    context = {
        "username" : str(req.user).capitalize(),
        "profile_pic" :profile_pic
    }

    if req.method == "POST":

        username = req.POST['username']
        profile_pic = req.FILES and req.FILES['post_file']

        if username and req.user.username != username:
            already_exist = User.objects.filter(Q(username = username) & ~Q(id = req.user.id))

            if not len(already_exist) > 0:
                user_model = User.objects.get(id = req.user.id)
                user_model.username = username
                user_model.save()

                context['message'] = 'Profile updated successfully'
                context['new_username'] = user_model.username
            else:
                context['error'] = 'Username already taken'
                return render(req,'edit_profile.html',context)
            
        if profile_pic:
            profile_pic_model = ProfilePic.objects.filter(user_id = req.user.id).first()

            if profile_pic_model:
                profile_pic_model.file = profile_pic
                profile_pic_model.save()
                context['message'] = 'Profile updated successfully'
            else:
                ProfilePic.objects.create(user_id = req.user.id,file = profile_pic)
                context['message'] = 'Profile updated successfully'

        return render(req,'edit_profile.html',context)
       

    else:
        

        return render(req,'edit_profile.html',context)