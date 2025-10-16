from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import (
    Client,
    Folder,
    File,
)
from django.shortcuts import redirect, render
from .forms import (
    FileUpload,
    CreateFolder,
    CreateUser,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re
# Create your views here.
def add_display_names(file_list):
    for item in file_list:
        item['name'] =  re.sub(r".*/", "", item['upload'])
    return file_list

def get_children(folder):
    parent = Folder.objects.get(id=folder)
    folders = Folder.objects.filter(parent=folder)
    files = File.objects.filter(folder=folder).values()
    children = []
    for child in folders:
        children.append(get_children(child.id))
    files = add_display_names(files)
    return {
        'id': folder,
        'name': parent.name,
        'folders': children,
        'files': list(files),
    }

@login_required
def details(request, id):
    file = File.objects.get(id=id)
    folder_name = Folder.objects.get(id=file.folder_id).name
    template = loader.get_template('filedetails.html')
    context = {
        'file': {
            'path': file.upload.url.split("/", 3)[3],
            'url': file.upload.url,
            'name': re.sub(r".*/", "", file.upload.url),
            'folder': folder_name
        }
    }
    return HttpResponse(template.render(context, request))

@login_required
def get_files(request):
    top_level = request.user.client.master
    context = {
        'main': get_children(top_level.id)
    }
    #pprint.pprint(context)
    template = loader.get_template("filetree.html")
    return HttpResponse(template.render(context, request))

@login_required
def add_files(request):
    if request.method == "POST":
        form = FileUpload(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/files/")
        else:
            print("Invalid Form")
    else:
        form = FileUpload(user=request.user)

    return render(request, "uploadfile.html", {"form": form})

@login_required
def add_folder(request):
    if request.method == "POST":
        form = CreateFolder(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/files/")
        else:
            print("Invalid request")
    else:
        form = CreateFolder(user=request.user)

    return render(request, "createfolder.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/login/")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
        else:
            messages.error(request, "The combination was not valid")
            return redirect('/login/')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/files/')
    else:
        form = CreateUser()
    return render(request, 'login.html', {"form": form})

def register(request):
    if request.method == "POST":
        form = CreateUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
        else:
            messages.error(request, "The combination was not valid")
            return redirect('/register/')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already in use")
            return redirect('/register/')
        
        user = User.objects.create_user(username=username)
        user.set_password(password)
        folder = Folder(name="home")
        folder.save()
        client = Client(user=user, master=folder)
        user.save()
        client.save()

        messages.info(request, "New account created!")
        return redirect('/login/')
    else:
        form = CreateUser()
    return render(request, 'register.html', {"form": form})

