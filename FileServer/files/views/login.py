from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
from ..models import ( 
    Folder,
    Client,
)
from django.contrib.auth.models import User
from ..forms import (
    CreateUser,
    LoginForm,
)

def logout_view(request):
    logout(request)
    return redirect("/login/")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
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
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {"form": form})

def register_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
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
        client = Client(user=user)
        user.save()
        client.save()
        folder = Folder(name="home", owner=client)
        folder.save()
        messages.info(request, "New account created!")
        return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'login/register.html', {"form": form})
