from django.urls import path
from . import views

app_name = "tracker"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:member_id>/', views.detail, name='detail'),
    path('event', views.event, name='event'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name="add_event"),
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
]