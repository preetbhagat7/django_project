from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from todolist_app import views
from .forms import CustomRegistrationForm
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        register_form=CustomRegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,"User create successfully.")
            return redirect("todolist")
            
    else:
        register_form=CustomRegistrationForm()
    return render(request, 'register.html', {'register_form':register_form})
      

def custom_logout(request):
    logout(request)  # clears the session
    return render(request, "index.html")  # show your custom page
    