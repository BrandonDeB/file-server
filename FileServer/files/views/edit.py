from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from ..models import (
    File,
)
from django.contrib.auth.decorators import login_required

@login_required
def edit(request, file_id):
    
    try:
        file = File.objects.get(id=file_id)
    except:
        return HttpResponseNotFound("Requested File does not exit")

    if not file.can_access(request.user.client):
        return HttpResponseForbidden("You do not have access to this file")

    if not file.is_editable():
        return HttpResponseForbidden("This file may not be edited")
    
    try:
        print(file.upload.path)
        with open(file.upload.path, "r") as reader:
            content = reader.read()
    except FileNotFoundError:
        return HttpResponseNotFound("File could not be read from server")

    context = {
        'name': file.upload.url,
        'contents': content,
        'id': file_id,
    }

    return render(request, "edit/mdedit.html", {"file": context})
