from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from .models import UserFile
from .forms import FileUploadForm
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm


def autorization(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/users/user_files')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/autorization.html', context)


def user_files(request):
    user = request.user
    user_files = UserFile.objects.filter(user=user)

    file_contents = []
    for file in user_files:
        if file.file.name.endswith('.txt'):  # Предположим, что вы хотите отображать только текстовые файлы
            with open(file.file.path, 'r') as f:
                content = f.read()
                file_contents.append({'name': file.name, 'content': content})

    return render(request, 'users/user_files.html', {'file_contents': file_contents})




def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations, now you are with us!')
            return HttpResponseRedirect('/')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.user = request.user
            new_file.save()
            return redirect('/users/user_files')
    else:
        form = FileUploadForm()
    return render(request, 'users/upload_file.html', {'form': form})

