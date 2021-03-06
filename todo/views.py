from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'The username has already taken! Please choose a new username'})
        else:
            # tell the user the passwords didn't match
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match! '})


def user_login(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(),
                                                           'error': 'Username and password do not match!'})
        else:
            login(request, user)
            return redirect('currentodos')


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currentodos(request):
    data = Todo.objects.filter(createdby=request.user, date_completed__isnull=True)
    return render(request, 'todo/currentodos.html', {'data': data})


@login_required
def completedtodos(request):
    data = Todo.objects.filter(createdby=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completedtodos.html', {'data': data})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.createdby = request.user
            newtodo.save()
            return redirect('currentodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Please try again'})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, createdby=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'data': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'data': todo, 'form': form, 'error':'Bad data passed in. Please try again'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, createdby=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('currentodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, createdby=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentodos')
