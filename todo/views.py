from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from datetime import date

class CustomUserForm(UserCreationForm):
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-2',
                'placeholder': field.label
            })


def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserForm()

    return render(request, 'signup.html', {'form': form})



@login_required
def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')

        Task.objects.create(
            user=request.user,
            title=title,
            due_date=due_date if due_date else None,
            priority=priority
        )

    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'home.html', {
        'tasks': tasks,
        'today': date.today()
    })


def complete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.completed = True
    task.save()
    return redirect('home')


def delete_task(request, id):
    task = Task.objects.get(id=id, user=request.user)
    task.delete()
    return redirect('home')