from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.template import loader

from .models import Member, Message, Event

from django.utils import timezone

from datetime import datetime

import requests
import json
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractYear

import calendar
import os
from dotenv import load_dotenv

load_dotenv()

@login_required
def index(request):
    test = Member.objects.all
    context = {
        'test': test,
    }
    return render(request, 'tracker/index.html', context)

@login_required
def detail(request, member_id):

    
    member = get_object_or_404(Member, pk=member_id)
    message_send = Message.objects.filter(id_member_id=member_id)
    message_count = message_send.count()

    all_months=list(calendar.month_name)
    all_months.remove('')
    print(all_months)

    data = message_send.annotate(month=ExtractMonth('date_message')).annotate(year=ExtractYear('date_message')).values('year','month').annotate(msg_count=Count('id_message')).order_by('month')
    
    
    data_dict = {month: 0 for month in all_months}

    for entry in data:
        month_name = calendar.month_name[entry['month']]
        data_dict[month_name] = entry['msg_count']

    print(data_dict)
    print(data)

    labels = list(data_dict.keys())
    messageCounts = list(data_dict.values())
    
    #for field in member._meta.get_fields():
    #    if hasattr(member, field.name):
    #        print(field.name, getattr(member, field.name))
    return render(request, 'tracker/detail.html', {'member': member, "message_count": message_count, 'labels': json.dumps(labels), 'data': json.dumps(messageCounts)})

@login_required
def event(request):
    all_events = Event.objects.all()
    context = {
        "events":all_events,
    }
    return render(request, "event/event.html", context)

@login_required
def all_events(request):
    all_events = Event.objects.all() 
    out = []
    for event in all_events:
        event.start_event = event.start_event.astimezone(timezone.get_current_timezone())
        event.end_event = event.end_event.astimezone(timezone.get_current_timezone())
        out.append({
            'title' : event.name_event,
            'id': event.id_event,
            'start': event.start_event.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end_event.strftime("%Y-%m-%d %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)

@login_required
def add_event(request):
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")

    webhook_url = os.environ.get('WEBHOOK_URL')
    # Informations sur l'événement à envoyer
    event_title = title
    print(start)
    parsed_datetime_start = datetime.fromisoformat(start)
    parsed_datetime_end = datetime.fromisoformat(end)

    if parsed_datetime_start.hour == 0 and parsed_datetime_end.hour == 0:
        format_date = "%d %b %Y"
    else:
        format_date = "%d %b %Y à %Hh%M"
    
    parsed_datetime_start = datetime.strftime(parsed_datetime_start, format_date)
    parsed_datetime_end= datetime.strftime(parsed_datetime_end, format_date)

  
    discord_message = {
        "content": "@everyone",
    }

    discord_message["embeds"] = [
        {
            "title": "Nouvelle évènement : " + event_title,
            "description": "description à venir",
            "url": "https://discordapp.com",
            "color": 344428,
            "footer": {
                "icon_url": "https://cdn.discordapp.com/embed/avatars/0.png",
                "text": ""
            },
            "fields": [
                {
                    "name": ":calendar:",
                    "value": "Début : " + parsed_datetime_start + "\nFin : " + parsed_datetime_start
                },
                
                {
                    "name": ":pushpin:",
                    "value": "Lieu à venir"
                }
            ]
        }
    ]
    response = requests.post(webhook_url, json = discord_message)
    event = Event(name_event=str(title), start_event=start, end_event=end)
    event.save()
    data = {}
    return JsonResponse(data)

@login_required
def update(request):

    
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")
    id = request.GET.get("id")

    start = datetime.strptime(start, "%d/%m/%Y %H:%M:%S")
    end = datetime.strptime(end, "%d/%m/%Y %H:%M:%S")

    event = Event.objects.get(id_event=id)
    event.start_event = start
    event.end_event = end
    if title :
        event.name_event = title
    event.save()
    data = {}
    return JsonResponse(data)
#, %H:%M:%S"
@login_required
def remove(request):
    id = request.GET.get("id")
    event = Event.objects.get(id_event=id)
    event.delete()
    data = {}
    return JsonResponse(data)