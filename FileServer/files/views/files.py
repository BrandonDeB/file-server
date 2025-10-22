from django.http import HttpResponse
from django.template import loader
from ..models import (
    Folder,
    File,
)
from django.shortcuts import redirect, render
from ..forms import (
    FileUpload,
    CreateFolder,
)
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
    template = loader.get_template('files/filedetails.html')
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
    template = loader.get_template("files/filetree.html")
    return HttpResponse(template.render(context, request))

@login_required
def add_files(request):
    if request.method == "POST":
        form = FileUpload(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            print("Invalid Form")
    else:
        form = FileUpload(user=request.user)

    return render(request, "files/uploadfile.html", {"form": form})

@login_required
def add_folder(request):
    if request.method == "POST":
        form = CreateFolder(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            print("Invalid request")
    else:
        form = CreateFolder(user=request.user)

    return render(request, "files/createfolder.html", {"form": form})

