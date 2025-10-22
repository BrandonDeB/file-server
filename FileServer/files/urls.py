from django.urls import path
from .views import (
    files,
    login,
    edit,
)

app_name = 'files'

urlpatterns = [
    path('', files.get_files, name='files'),
    path('file/<int:id>', files.details, name='details'),
    path('file/upload/', files.add_files, name='upload'),
    path('folder/add/', files.add_folder, name='folder_add'),
    path('login/', login.login_view, name='login'),
    path('register/', login.register_view, name='register'),
    path('logout/', login.logout_view, name='logout'),
    path('file/edit/<int:file_id>', edit.edit, name='edit'),
]
