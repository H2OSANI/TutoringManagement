from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/register')
        else:
            messages.success(request, "Fehler")
    else:
        return render(request, 'Login/index.html', {})


def register(request):
    return render(request, 'Login/register.html')
