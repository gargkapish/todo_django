from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

# Create your views here.

def home(request):
    tasks = Task.objects.all()
    return render(request, 'home.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
        )
        return redirect('home')
    return render(request, 'add_task.html')


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.done = 'done' in request.POST
        task.save()
        return redirect('home')
    return render(request, 'edit_task.html', {'task': task})


def toggle_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.done = not task.done
        task.save()
    return redirect('home')


def delete_task(request, task_id):
    if request.method == 'POST':
        get_object_or_404(Task, id=task_id).delete()
    return redirect('home')
