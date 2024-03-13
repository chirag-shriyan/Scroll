from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myauth.models import ProfilePic
from .models import Chat_Room as Chat_Room_Model

# Create your views here.

@login_required(login_url = '/login')
def Lobby(req):

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

        return render(req,'lobby.html',context)

    return render(req,'lobby.html',{"profile_pic":profile_pic})

import uuid

@login_required(login_url = '/login')
def Chat_Room(req,username):

    
    user = User.objects.filter(username = username).first()
    profile_pic = ProfilePic.objects.filter(user_id = user.id).first()

    room_id =  Chat_Room_Model.objects.filter(Q(user1_id = req.user.id) & Q(user2_id = user.id) | Q(user1_id = user.id) & Q(user2_id = req.user.id)).first()
    if room_id:
        room_id = room_id.room_id
    else:
        room_id = Chat_Room_Model.objects.create(user1_id =  req.user.id,user2_id = user.id,room_id = uuid.uuid4()).room_id

    if profile_pic:
        profile_pic = {"file": profile_pic.file , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}

    username = username.capitalize()

    context = {
        "username":username,
        "room_id":room_id,
        "profile_pic": profile_pic,
    }

    return render(req,'chat_room.html',context)