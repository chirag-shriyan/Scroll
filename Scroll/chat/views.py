from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from myauth.models import ProfilePic
from .models import Chat_Room as Chat_Room_Model, Notification as Notification_Model,Message
from django.views.decorators.cache import never_cache

# Create your views here.

@login_required(login_url = '/login')
@never_cache
def Lobby(req):

    search = req.GET.get('q')
    profile_pic = ProfilePic.objects.filter(user_id = req.user.id).values().first()

    if profile_pic:
        profile_pic = {"file": profile_pic['file'] , "exist": True}
    else:
        profile_pic = {"file": 'images/profile.jpg', "exist": False}


    if search:
        SEARCH_DATA = User.objects.filter(Q(username__contains = search) & ~Q(id = req.user.id)).values().order_by('-date_joined')
        not_found = False

        if len(SEARCH_DATA) > 0:
            for user in SEARCH_DATA:
                user_profile_pic = ProfilePic.objects.filter(user_id = user['id']).values().first()
                
                if user_profile_pic:
                    user['profile_pic'] = {"file": user_profile_pic['file'] , "exist": True}
                else:
                    user['profile_pic'] = {"file": 'images/profile.jpg', "exist": False}
        else:
            not_found = True

        context = {
            "search_data": SEARCH_DATA,
            "not_found": not_found,
            "profile_pic": profile_pic,
        }

        return render(req,'lobby.html',context)
    else:
        CHAT_DATA = Chat_Room_Model.objects.filter(Q(user1 = req.user.id) | Q(user2 = req.user.id)).order_by('-updated_at')
        data_list = []

        for user in CHAT_DATA:
            temp = user.user2 if user.user1 == req.user else user.user1
            temp.last_message = user.last_message
            temp.room_id = user.room_id
            if temp.last_message:
                data_list.append(temp)
   
        if len(data_list) > 0:
            for user in data_list:
                user_profile_pic = ProfilePic.objects.filter(user_id = user.id).values().first()
                notification_data = Notification_Model.objects.filter(Q(user_id = req.user.id) & Q(room_id = user.room_id)).first()

                if user_profile_pic:
                    user.profile_pic = {"file": user_profile_pic["file"] , "exist": True}
                else:
                    user.profile_pic = {"file": 'images/profile.jpg', "exist": False}

                if notification_data:
                    notification_data.is_notification = False
                    notification_data.save()
                    if notification_data.num_of_notifications > 0:
                        if notification_data.num_of_notifications < 9:
                            user.num_of_notifications = {"num":notification_data.num_of_notifications ,"more_then_nine": False}
                        else:
                            user.num_of_notifications = {"num":9 ,"more_then_nine": True}

        context = {
            "chat_data": data_list,
            "profile_pic": profile_pic,
        }

        return render(req,'lobby.html',context)
    

import uuid

@login_required(login_url = '/login')
def Chat_Room(req,username):
    send_to_user = User.objects.filter(username = username).first()

    if send_to_user:
        profile_pic = ProfilePic.objects.filter(user_id = send_to_user.id).first()

        if profile_pic:
            profile_pic = {"file": profile_pic.file , "exist": True}
        else:
            profile_pic = {"file": 'images/profile.jpg', "exist": False}

        room_id =  Chat_Room_Model.objects.filter(Q(user1_id = req.user.id) & Q(user2_id = send_to_user.id) | Q(user1_id = send_to_user.id) & Q(user2_id = req.user.id)).first()

        if room_id:
            room_id = room_id.room_id
        else:
            room_id = Chat_Room_Model.objects.create(user1_id =  req.user.id,user2_id = send_to_user.id,room_id = uuid.uuid4()).room_id

        NOTIFICATION_DATA = Notification_Model.objects.filter(Q(user_id = req.user.id) & Q(room_id = room_id)).first()
        if NOTIFICATION_DATA:
            NOTIFICATION_DATA.num_of_notifications = 0
            NOTIFICATION_DATA.is_notification = False
            NOTIFICATION_DATA.save()

        chats = Message.objects.filter(Q(sender_id = req.user.id) & Q(receiver_id = send_to_user.id) | Q(sender_id = send_to_user.id) & Q(receiver_id = req.user.id)).order_by('created_at')

        for chat in chats:
            if chat.is_unread:
                chat.is_unread = False
                chat.save()
                chat.is_unread = True

        username = username.capitalize()

        context = {
            "username":username,
            "send_to_user":send_to_user,
            "room_id":room_id,
            "profile_pic": profile_pic,
            "chats": chats,
        }

        return render(req,'chat_room.html',context)
    else:
        return render(req,'not_found.html')
    

import json
from django.http import JsonResponse 

@login_required(login_url = '/login')
def Add_Messages(req):

    if req.method == 'POST':
        body = json.loads(req.body)
        message = body['message']
        receiver = body['receiver']
        room_id = body['room_id']

        if message and receiver:
            chat_room = Chat_Room_Model.objects.filter(room_id = room_id).first()
            notification = Notification_Model.objects.filter(Q(user_id = receiver) & Q(room_id = room_id)).first()

            if notification:
                notification.num_of_notifications += 1
                notification.is_notification = True
                notification.save()
            else:
                Notification_Model.objects.create(user_id = receiver,room_id = room_id,num_of_notifications = 1, is_notification = True)


            if len(message) > 10:
                chat_room.last_message = message[0:30] + '...'
            else:
                chat_room.last_message = message
            chat_room.save()

            message = Message.objects.create(sender_id = req.user.id,receiver_id = receiver,message = message)
            return JsonResponse({
                "status":200,
                "message":'Message successfully added',
                "message_id":message.id
            })
        else:
            return JsonResponse({
                "status":401,
                "message":'Bad request'
            })
    else:
        return render(req,'not_found.html')
    
@login_required(login_url = '/login')
def Notifications(req):
    
    if req.method == "GET":
        notifications = Notification_Model.objects.filter(Q(user_id = req.user.id) & Q(Q(is_notification = True) | Q(num_of_notifications__gt = 0)))
        data = list(notifications.values())

        for element in data:
            last_message = Chat_Room_Model.objects.filter(Q(room_id = element['room_id'])).first().last_message
            element['last_message'] = last_message
    

        return JsonResponse({
            "status": 200,
            "data": data
        })
    
@login_required(login_url = '/login')
def Clear_Notifications(req):
    
    if req.method == "GET":
        room_id = req.GET.get('room_id')

        if room_id:
            notifications = Notification_Model.objects.filter(Q(user_id = req.user.id) & Q(room_id = room_id))
            data = list(notifications.values())

            for notification in notifications:
                notification.is_notification = False
                notification.num_of_notifications = 0
                notification.save()
            
            return JsonResponse({
                "status": 200,
                "data": data
            })
        else:
            notifications = Notification_Model.objects.filter(Q(user_id = req.user.id))
            for notification in notifications:
                notification.is_notification = False
                notification.save()

            return JsonResponse({
                "status": 200,
            })

       

        
@login_required(login_url = '/login')
def Get_Room_Id(req):
    
    if req.method == "GET":
        room_ids =  Chat_Room_Model.objects.filter(Q(user1_id = req.user.id) | Q(user2_id = req.user.id))
        data = []

        for id in room_ids:
            if id:
                data.append(id.room_id)

        return JsonResponse({
            "status": 200,
            "data": data
        })
        
