from django.shortcuts import render
from .forms import PostForm
from .models import Post,Post_Like,Post_Comment
from myauth.models import ProfilePic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login')
def Post_View(req,post_id=None):

    if post_id:
        DATA = Post.objects.filter(Q(post_id = post_id) & (Q(is_public = True) | Q(user_id = req.user.id))).values().first()

        if DATA:
            is_owner = DATA['user_id'] == req.user.id

            added_by = str(User.objects.get(id = DATA['user_id'])).capitalize()
            added_by_url = '/users/' + User.objects.get(id = DATA['user_id']).username 
            added_by_profile = ProfilePic.objects.filter(user_id = DATA['user_id']).values().first()
            is_liked = Post_Like.objects.filter(Q(user_id = req.user.id) & Q(post_id = DATA['post_id'])).first()
    
            DATA['added_by'] = added_by
            DATA['added_by_url'] = added_by_url or '#'

            if added_by_profile:
                DATA['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
            else:
                DATA['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}
            
            if is_liked:
                DATA['is_liked'] = True
            else:
                DATA['is_liked'] = False

            COMMENT_DATA = Post_Comment.objects.filter(post_id = post_id).values().order_by('-created_at')

            for comment in COMMENT_DATA:
                added_by = User.objects.get(id = comment['user_id']).username.capitalize()
                added_by_profile = ProfilePic.objects.filter(user_id = comment['user_id']).values().first()

                comment['added_by'] = added_by
                if added_by_profile:
                    comment['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
                else:
                    comment['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

            context = {
                "data": DATA,
                "comment_data": COMMENT_DATA,
                "is_owner": is_owner,
            }

            return render(req,'post.html',context)
        else:
            return render(req,'not_found.html')
    
    else:
        return render(req,'not_found.html')
    

import json
from django.http import JsonResponse
import math

def Get_Posts(req):

    if req.method == 'POST':
        body = json.loads(req.body)
        total_num_posts = body['total_num_posts']
        posts_limit = body['posts_limit']
        current_page = body['current_page']
  
        if current_page < math.ceil(total_num_posts / posts_limit):
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


@login_required(login_url='/login')
def Create_Posts(req):
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    if req.method == 'POST':
        form = PostForm(req.POST,req.FILES)

        if form.is_valid():
            post_file = req.FILES['post_file']
            post_bio = req.POST['post_bio']
            post_type = req.POST['post_type']

            Post.objects.create(user_id = req.user.id,file = post_file,bio = post_bio,is_public = post_type)
            message = 'Post uploaded successfully'

            return render(req,'create_posts.html' , {"message":message, "profile_pic":profile_pic})
        else:
            error = 'Something went wrong try again'
            return render(req,'create_posts.html' , {"error":error, "profile_pic":profile_pic})

    else:
        return render(req, 'create_posts.html',{"profile_pic":profile_pic})


@login_required(login_url='/login')
def Like_Posts(req):
    
    if req.method == "POST":
        body = json.loads(req.body)
        is_liked = Post_Like.objects.filter(Q(user_id = req.user.id) & Q(post_id = body['post_id'])).first()
        
        if is_liked == None:
            current_likes = len(Post_Like.objects.filter(post_id = body['post_id']).values())
            # post_id = Post.objects.filter(post_id = body['post_id']).first()

            Post_Like.objects.create(user_id = req.user.id,post_id = body['post_id'])

            current_post = Post.objects.filter(post_id = body['post_id']).first()
            current_post.num_of_likes = current_likes + 1
            current_post.save()

            return JsonResponse({
                "status":200,
                "is_liked":True,
                "current_likes": current_post.num_of_likes,
            })
        else:
            current_likes = len(Post_Like.objects.filter(post_id = body['post_id']).values())
            is_liked.delete()

            current_post = Post.objects.filter(post_id = body['post_id']).first()
            current_post.num_of_likes = current_likes - 1
            current_post.save()

            return JsonResponse({
                "status":200,
                "is_liked":False,
                "current_likes":current_post.num_of_likes,
            })

    return render(req,'not_found.html')


@login_required(login_url='/login')
def Comment_Posts(req):
    
    if req.method == "POST":
        body = json.loads(req.body)
        post_id = body['post_id']
        comment = body['comment']

        Post_Comment.objects.create(post_id = post_id,user_id = req.user.id,comment=comment)

        comment_data = Post_Comment.objects.filter(post_id = post_id).order_by('-created_at').values()

        for comment in comment_data:
                added_by = User.objects.get(id = comment['user_id']).username.capitalize()
                added_by_profile = ProfilePic.objects.filter(user_id = comment['user_id']).values().first()

                comment['added_by'] = added_by
                if added_by_profile:
                    comment['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
                else:
                    comment['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

        if len(comment_data) > 0:
            comment_data = list(comment_data)

        return JsonResponse({
            "status":200,
            "post_id": body['post_id'],
            "comment_data": comment_data,
        })

    return render(req,'not_found.html')


@login_required(login_url='/login')
def Post_Edit(req,post_id = None):
    post_model = Post.objects.get(post_id = post_id)

    if post_model.user_id == req.user.id:
        profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

        if profile_pic:
            profile_pic = {"file": profile_pic['file'] , "exist": True}
        else:
            profile_pic = {"file": 'images/profile.jpg', "exist": False}

        context = {
            "username" : str(req.user).capitalize(),
            "post_id" : post_id,
            "profile_pic" : profile_pic,
            "bio" : post_model.bio,
            "is_public" : bool(post_model.is_public),
        }
    
        if req.method == "POST":
            post_bio = req.POST['post_bio']
            post_type = req.POST['post_type']

            if post_bio != post_model.bio:
                post_model.bio = post_bio
                post_model.save()

                context['message'] = 'Post updated successfully'
                context['bio'] = post_model.bio

            if post_type == 'True' and post_model.is_public == False:
                post_model.is_public = True
                post_model.save()

                context['is_public'] = post_model.is_public
                context['message'] = 'Post updated successfully'
            elif post_type == 'False' and post_model.is_public == True:
                post_model.is_public = False
                post_model.save()

                context['is_public'] = post_model.is_public
                context['message'] = 'Post updated successfully'

            return render(req,'edit_post.html',context)
        else:
            return render(req,'edit_post.html',context)
    else:
        return render(req,'not_found.html')


from pathlib import Path
import os 

@login_required(login_url='/login')
def Post_Delete(req):

    if req.method == "POST":
        body = json.loads(req.body)
        post_id = body['post_id']

        if post_id:
            post_data = Post.objects.filter(Q(post_id = post_id) & Q(user_id = req.user.id)).first()
           
            if post_data:
                post_data.delete()
                file_to_delete = Path.cwd() / 'uploads' / str(post_data.file)
                if os.path.exists(file_to_delete):
                    os.remove(file_to_delete)

                return JsonResponse({
                    "status": 200,
                    "message": 'Post deleted successfully',
                })
            else:
                return JsonResponse({
                    "status": 401,
                    "message": 'Unauthorized request',
                })

        else:
            return JsonResponse({
                "status": 400,
                "message": 'Bad request',
            })

    return render(req,'not_found.html')