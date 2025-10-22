from django.shortcuts import render

def edit(request, file_id):
    return render(request, "edit/mdedit.html", {"file_id": file_id})
