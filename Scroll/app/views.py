from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from posts.models import Post,Post_Like
from myauth.models import ProfilePic
from django.db.models import Q

# Create your views here.

@login_required(login_url = '/login')
def Index(req):
   
    username = str(req.user).capitalize()
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()
    posts_limit = 5

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    total_num_posts = Post.objects.filter(is_public = True).order_by('-created_at').count()
    POST_DATA = Post.objects.filter(is_public = True).order_by('-created_at').values()[0:posts_limit]

    if total_num_posts <= 0:
        no_posts_found = True
    else:
        no_posts_found = False

    for post in POST_DATA:
        added_by = str(User.objects.get(id = post['user_id'])).capitalize()
        added_by_url = '/users/' + User.objects.get(id = post['user_id']).username 
        added_by_profile = ProfilePic.objects.filter(user_id = post['user_id']).values().first()
        is_liked = Post_Like.objects.filter(Q(user_id = req.user.id) & Q(post_id = post['post_id'])).first()
      
        post['added_by'] = added_by
        post['added_by_url'] = added_by_url or '#'

        if added_by_profile:
            post['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
        else:
            post['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

        if is_liked:
            post['is_liked'] = True
        else:
            post['is_liked'] = False
        
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
        "total_num_posts" : total_num_posts,
        "posts_limit" : posts_limit,
        "no_posts_found":no_posts_found,
        "suggestions_data" : SUGGESTIONS_DATA,
        "no_suggestions_data" : no_suggestions_data,
    }
    return render(req,'index.html',context)


import json
from django.http import JsonResponse

def Get_Posts(req):

    if req.method == 'POST':
        body = json.loads(req.body)
        total_num_posts = body['total_num_posts']
        posts_limit = body['posts_limit']
        current_page = body['current_page']
  
        if current_page < total_num_posts // posts_limit:
            skip = posts_limit * current_page

            POST_DATA = Post.objects.filter(is_public = True).order_by('-created_at').values()[skip: skip + posts_limit]
            for post in POST_DATA:
                added_by = str(User.objects.get(id = post['user_id'])).capitalize()
                added_by_url = '/users/' + User.objects.get(id = post['user_id']).username 
                added_by_profile = ProfilePic.objects.filter(user_id = post['user_id']).values().first()
                is_liked = Post_Like.objects.filter(Q(user_id = req.user.id) & Q(post_id = post['post_id'])).first()
            
                post['added_by'] = added_by
                post['added_by_url'] = added_by_url or '#'

                if added_by_profile:
                    post['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
                else:
                    post['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

                if is_liked:
                    post['is_liked'] = True
                else:
                    post['is_liked'] = False
                    
            return JsonResponse({
                "status":200,
                "current_page" : current_page + 1,
                "posts_data" : list(POST_DATA),
                "more_post" : True
            })
        else:
            return JsonResponse({
                "status":200,
                "more_post" : False
            })

    return render(req,'not_found.html')