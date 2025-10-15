from django.contrib import admin
from .models import (
    File,
    User,
    Folder,
)
# Register your models here.
admin.site.register(File)
admin.site.register(User)
admin.site.register(Folder)
