from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('<slug:roomcode>/', views.room, name='room')
]
