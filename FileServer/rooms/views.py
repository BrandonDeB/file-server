from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def room(request, roomcode):
    return render(request, "room.html", {"code": roomcode})
