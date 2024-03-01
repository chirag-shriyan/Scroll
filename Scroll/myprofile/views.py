from django.shortcuts import render
from django.contrib.auth.models import User
from myauth.models import ProfilePic
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