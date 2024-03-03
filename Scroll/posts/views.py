from django.shortcuts import render
from .forms import PostForm
from .models import Post,Post_Like
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

            context = {
                "data": DATA
            }

            return render(req,'post.html',context)
        else:
            return render(req,'not_found.html')
    
    else:
        return render(req,'not_found.html')

# @login_required(login_url='/login')
def Create_Posts(req):

    if req.method == 'POST':
        form = PostForm(req.POST,req.FILES)

        if form.is_valid():
            post_file = req.FILES['post_file']
            post_bio = req.POST['post_bio']
            post_type = req.POST['post_type']

            Post.objects.create(user_id = req.user.id,file = post_file,bio = post_bio,is_public = post_type)
            message = 'Post uploaded successfully'

            return render(req,'create_posts.html' , {"message":message})
        else:
            error = 'Something went wrong try again'
            return render(req,'create_posts.html' , {"error":error})

    else:
        return render(req, 'create_posts.html')
    
import json
from django.http import JsonResponse

@login_required(login_url='/login')
def Like_Posts(req):
    
    if req.method == "POST":
        body = json.loads(req.body)
        is_liked = Post_Like.objects.filter(Q(user_id = req.user.id) & Q(post_id = body['post_id'])).first()
        
        if is_liked == None:
            current_likes = len(Post_Like.objects.filter(post_id = body['post_id']).values())
            post_id = Post.objects.filter(post_id = body['post_id']).first()

            Post_Like.objects.create(user_id = req.user.id,post_id = post_id)

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