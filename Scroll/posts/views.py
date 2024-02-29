from django.shortcuts import render
from .forms import PostForm
from .models import Post

# Create your views here.

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