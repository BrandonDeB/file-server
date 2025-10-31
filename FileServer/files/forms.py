from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import (
    File,
    Folder,
)
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

def get_folders(folder):
    stack = [folder]
    children = []
    while len(stack) > 0:
        child = stack.pop()
        children.append(child)
        stack.extend(Folder.objects.filter(parent=child))
    print(children)
    return children

def get_master(user):
    return Folder.objects.filter(owner=user.client, parent__isnull=True).first()

class FileUpload(ModelForm):
    class Meta:
        model = File
        fields = ["folder", "upload", "file_type", "shared_with"]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            folders = get_folders(get_master(user))
            self.fields['folder'].queryset = Folder.objects.filter(id__in=[f.id for f in folders])
            self.fields['folder'].empty_label = None
            self.fields['shared_with'].queryset = (
                self.fields['shared_with'].queryset.exclude(id=user.id)
            )

class CreateFolder(ModelForm):
    class Meta:
        model = Folder
        fields = ["name", "parent"]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            folders = get_folders(get_master(user))
            self.fields['parent'].queryset = Folder.objects.filter(id__in=[f.id for f in folders])
            self.fields['parent'].empty_label = None

class CreateUser(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
    
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ))
