from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JoinRoomForm

@login_required
def room(request, roomcode):
    return render(request, "room.html", {"code": roomcode, "user": request.user.username})

@login_required
def join_room(request):
    if request.method == "POST":
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['room_code']
            return redirect('/rooms/'+code)
    else:
        form = JoinRoomForm()

    return render(request, 'join.html', {'form': form})
