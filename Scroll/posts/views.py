from django.shortcuts import render
from .forms import PostForm
from .models import Post
from myauth.models import ProfilePic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def Post_View(req,post_id=None):

    if post_id:
        DATA = Post.objects.filter(post_id = post_id).values().first()
        if DATA:
            added_by = str(User.objects.get(id = DATA['user_id'])).capitalize()
            added_by_profile = ProfilePic.objects.filter(user_id = DATA['user_id']).values().first()

            DATA['added_by'] = added_by
            if added_by_profile:
                DATA['added_by_profile'] = {"file": added_by_profile['file'] , "exist": True}
            else:
                DATA['added_by_profile'] = {"file": 'images/profile.jpg' , "exist": False}

            context = {
                "data": DATA
            }

            return render(req,'post.html',context)
        else:
            return render(req,'not_found.html')
    
    else:
        return render(req,'not_found.html')

@login_required(login_url='/login')
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