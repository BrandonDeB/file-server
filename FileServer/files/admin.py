from django.contrib import admin
from .models import (
    File,
    User,
    Folder,
)
from .forms import FileUpload
# Register your models here.
admin.site.register(File)
admin.site.register(User)
admin.site.register(Folder)
