from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import (
    Folder,
    File,
)
from django.shortcuts import render
from .forms import (
    FileUpload,
    CreateFolder,
)
import pprint
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

def details(request, id):
    file = File.objects.get(id=id)
    folder_name = Folder.objects.get(id=file.folder_id).name
    template = loader.get_template('filedetails.html')
    context = {
        'file': {
            'path': file.upload.url.split("/", 3)[3],
            #'path': file.upload.url,
            'name': re.sub(r".*/", "", file.upload.url),
            'folder': folder_name
        }
    }
    return HttpResponse(template.render(context, request))

def get_files(request):
    context = {
        'main': get_children(1)
    }
    #pprint.pprint(context)
    template = loader.get_template("filetree.html")
    return HttpResponse(template.render(context, request))


def add_files(request):
    if request.method == "POST":
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/files/")
        else:
            print("Invalid Form")
    else:
        form = FileUpload()

    return render(request, "uploadfile.html", {"form": form})

def add_folder(request):
    if request.method == "POST":
        form = CreateFolder(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/files/")
        else:
            print("Invalid request")
    else:
        form = CreateFolder()

    return render(request, "createfolder.html", {"form": form})
