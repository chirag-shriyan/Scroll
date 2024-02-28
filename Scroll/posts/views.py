from django.shortcuts import render
from .forms import PostForm
from .models import Post

# Create your views here.

def Create_Posts(req):

    if req.method == 'POST':
        form = PostForm(req.POST)
        print(form)
    else:
        print(Post.objects.all().values())
        return render(req, 'Hello')