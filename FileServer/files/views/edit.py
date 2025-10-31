from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render
from ..models import (
    File,
)
from django.contrib.auth.decorators import login_required
from django.template import loader

error_template = loader.get_template('errors/basicerror.html')

@login_required
def edit(request, file_id):
    
    try:
        file = File.objects.get(id=file_id)
    except:
        error = {
            'context': {
                    'title': "Does not exist",
                    'error_message': "You are trying to access a file that does not exist"
                }
        }
        return HttpResponseNotFound(error_template.render(error,request))

    if not file.can_access(request.user.client):
        error = {
            'context': {
                    'title': "No access",
                    'error_message': "You are trying to access a file that is not owned or shared with you"
                }
        }
        return HttpResponseForbidden(error_template.render(error,request))

    if not file.is_editable():
        error = {
            'context': {
                    'title': "Not editable",
                    'error_message': "You are trying to edit a file that may not be edited"
                }
        }
        return HttpResponseForbidden(error_template.render(error, request))
    
    try:
        print(file.upload.path)
        with open(file.upload.path, "r") as reader:
            content = reader.read()
    except FileNotFoundError:
        error = {
            'context': {
                    'title': "Unreadable",
                    'error_message': "The file you are looking for cannot be found in the server"
                }
        }
        return HttpResponseNotFound(error_template.render(error, request))

    context = {
        'name': file.upload.url,
        'contents': content,
        'id': file_id,
    }

    return render(request, "edit/mdedit.html", {"file": context})
