from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from todolist_app.models import Task
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    return render(request,"index.html", {})

@login_required
def todolist(request):
    
    if request.method == "POST":
        form_data=TaskForm(request.POST or None)
        if form_data.is_valid():            
            instance=form_data.save(commit=False)
            instance.Owner = request.user
            instance.save()
            messages.success(request, "Task added Successfully.")
            return redirect("todolist")
        else:
            form_data=TaskForm()
            messages.success(request, "Something went wrong!")
        
        
    all_tasks = Task.objects.filter(Owner=request.user)
    paginator=Paginator(all_tasks, 8)
    page = request.GET.get("page")
    all_tasks=paginator.get_page(page)
    context = {
        'page' : 'Todolist',
        'all_tasks' :  all_tasks,
    }
    return render(request,"todolist.html", context)
@login_required
def delete_task(request, task_id):
    task_obj = Task.objects.get(id=task_id)
    if task_obj.Owner==request.user:
            task_obj.delete()
            messages.success(request, f"Task -{task_obj.task} Deleted")
    else:
        messages.error(request,f"Acces Denied")
    return redirect("todolist")
@login_required
def edit_task(request, task_id):
    task_obj = Task.objects.get(id=task_id)
    if request.method == "POST":
        form_data = TaskForm(request.POST or None, instance=task_obj)
        if form_data.is_valid:
            form_data.save()
            messages.success(request, "Task Updated !!")
            return redirect("todolist")
        messages.success(request,"Error encountered in task updation !!")
    else:
        context ={
        'task_obj' : task_obj
        }
    return render(request,"edit.html", context)
@login_required
def pending_task(request, task_id):
    task_obj = Task.objects.get(id=task_id)
    if task_obj.Owner==request.user:
            task_obj.is_completed = False
            task_obj.save()
            messages.success(request, f"Status Changed!!")
    else:
        messages.error(request, f"You are not allowed to change the status!!")
    return redirect("todolist")

@login_required
def complete_task(request, task_id):
    task_obj = Task.objects.get(id=task_id)
    if task_obj.Owner==request.user:
        task_obj.is_completed = True
        task_obj.save()
        messages.success(request, f"Status Changed!!")
    else:
        messages.error(request, f"You are not allowed to change the status!!")
    return redirect("todolist")



def contact(request):
    context = {
        'page' : 'Contact'
    }
    return render(request,"contact.html", context)

def about(request):
    context = {
        'page' : "About Section"
    }
    return render(request,"about.html", context)