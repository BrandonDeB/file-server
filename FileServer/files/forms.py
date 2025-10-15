from django.forms import ModelForm
from .models import (
    File,
    Folder,
)

class FileUpload(ModelForm):
    class Meta:
        model = File
        fields = "__all__"

class CreateFolder(ModelForm):
    class Meta:
        model = Folder
        fields = "__all__"
