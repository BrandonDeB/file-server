from django.urls import path
from . import views

urlpatterns = [
    path('files/', views.get_files, name='files'),
    path('files/file/<int:id>', views.details, name='details'),
    path('files/upload/', views.add_files, name='upload'),
    path('folders/add/', views.add_folder, name='folder_add'),
]
