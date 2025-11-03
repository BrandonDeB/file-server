from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('<slug:roomcode>/', views.room, name='room'),
    path('', views.join_room, name='join_room')
]
