from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import (
    File,
    Folder,
)

def get_folders(folder):
    stack = [folder]
    children = []
    while len(stack) > 0:
        child = stack.pop()
        children.append(child)
        stack.extend(Folder.objects.filter(parent=child))
    print(children)
    return children

class FileUpload(ModelForm):
    class Meta:
        model = File
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            master = user.client.master
            folders = get_folders(master)
            self.fields['folder'].queryset = Folder.objects.filter(id__in=[f.id for f in folders])

class CreateFolder(ModelForm):
    class Meta:
        model = Folder
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            master = user.client.master
            folders = get_folders(master)
            self.fields['parent'].queryset = Folder.objects.filter(id__in=[f.id for f in folders])

class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
