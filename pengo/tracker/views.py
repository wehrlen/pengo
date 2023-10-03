from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.template import loader

from .models import Member, Message, Event

@login_required
def index(request):
    test = Member.objects.all
    print(type(test))
    context = {
        'test': test,
    }
    return render(request, 'tracker/index.html', context)

@login_required
def detail(request, member_id):
    
    member = get_object_or_404(Member, pk=member_id)
    message_send = Message.objects.filter(id_member_id=member_id)
    print(message_send)
    message_count = message_send.count()
    print(message_count)


    # Parcours de l'objet récupéré
    for field in member._meta.get_fields():
        if hasattr(member, field.name):
            print(field.name, getattr(member, field.name))
    return render(request, 'tracker/detail.html', {'member': member, "message_count": message_count})

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
        out.append({
            'title' : event.name_event,
            'id': event.id_event,
            'start': event.start_event.strftime("%Y-%m-%d %H:%M:%S"),
            'end': event.end_event.strftime("%Y-%m-%d %H:%M:%S"),
        })
    print(out)
    return JsonResponse(out, safe=False)

@login_required
def add_event(request):
    print("test")
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")

    print(title)
    print(start)
    print(end)

    event = Event(name_event=str(title), start_event=start, end_event=end)
    event.save()
    data = {}
    return JsonResponse(data)

def update(request):
    title = request.GET.get("title")
    start = request.GET.get("start")
    end = request.GET.get("end")
    id = request.GET.get("id")
    event = Event.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)
#, %H:%M:%S"