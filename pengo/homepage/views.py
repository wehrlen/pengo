from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UsernameChangeForm
from django.contrib.auth import update_session_auth_hash

from tracker.models import Member, Message, Channel, Roles, Server

import json
# Create your views here.

@login_required
def home(request):
    test= Member.objects.all
    test2 = Member.objects.all()
    Servers = Server.objects.filter(name_guild="ANIME GETAWAY").values_list("name_guild", flat= True)[0]
    members= Member.objects.all().count()
    messages =  Message.objects.all().count()
    channels =  Channel.objects.all()
    roles = Roles.objects.all().count()
    
    data = []
    data_channel = []


    for e in test2:
        messages_count = Message.objects.filter(id_member_id=e.id_member).count()
        print(messages_count)
        data.append({'nom': e.name_member, 'messages': messages_count})

    for e in channels:
        messages_count = Message.objects.filter(id_channel_id=e.id_channel).count()
        print(messages_count)
        data_channel.append({'nom': e.name_channel, 'messages': messages_count})
    print(data_channel)

    context = {
        'test': test,
        "messages" : messages,
        "channels" : channels.count(),
        "roles" : roles,
        "members" : members,
        "servers" : Servers,
        "data": json.dumps(data),
        "data_channel": json.dumps(data_channel)

    }
    return render(request, 'homepage/home.html', context)

@login_required
def user(request):

    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        user_form = UsernameChangeForm(data=request.POST, instance=request.user)
        
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('/user')
        elif user_form.is_valid():
            user_form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès")
            return redirect('/user')  
 

    else:
        password_form = PasswordChangeForm(user=request.user)
        user_form = UsernameChangeForm(instance=request.user)
    context = {
        'password_form': password_form,
        'user_form': user_form,
    }
    return render(request, 'homepage/user.html', context)