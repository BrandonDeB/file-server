from django.http import FileResponse, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
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
import os

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

def get_file_name(upload):
    return re.sub(r".*/", "", upload.url)

@login_required
def download_file(request, file_id):
    try:
        file = File.objects.get(id=file_id)
    except:
        return HttpResponseNotFound("Requested file does not exist")
    
    if not file.can_access(request.user.client):
        return HttpResponseForbidden("You do not have access to this file")

    file_path = file.upload.path
    if not os.path.exists(file_path):
        return HttpResponseNotFound("File not in server storage")

    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def details(request, id):
    file = File.objects.get(id=id)

    if not file.can_access(request.user.client):
        return HttpResponseForbidden("You do not have access to this file")

    folder_name = Folder.objects.get(id=file.folder_id).name
    template = loader.get_template('files/filedetails.html')
    context = {
        'file': {
            'path': file.upload.url.split("/", 3)[3],
            'url': file.upload.url,
            'name': get_file_name(file.upload),
            'folder': folder_name,
            'type': file.file_type,
            'id': file.id,
        }
    }
    return HttpResponse(template.render(context, request))

@login_required
def get_files(request):
    top_level = Folder.objects.filter(owner=request.user.client, parent__isnull=True).first()
    shared = File.objects.filter(shared_with=request.user.client)
    for file in shared:
        file.name = get_file_name(file.upload)
    context = {
        'main': get_children(top_level.id),
        'shared': shared,
    }
    #pprint.pprint(context)
    template = loader.get_template("files/filetree.html")
    return HttpResponse(template.render(context, request))

@login_required
def add_files(request):
    if request.method == "POST":
        form = FileUpload(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user.client
            file.save()
            form.save_m2m()
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
            folder = form.save(commit=False)
            folder.owner = request.user.client
            folder.save()
            return redirect("/")
        else:
            print("Invalid request")
    else:
        form = CreateFolder(user=request.user)

    return render(request, "files/createfolder.html", {"form": form})

