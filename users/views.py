from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from .models import UserFile
from .forms import UserFileForm
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import UserFile, SharedWith  # Убедитесь, что здесь импортирован SharedWith
from django.db.models import Q




def autorization(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect('/users/files')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/autorization.html', context)




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



def user_files(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()

            shared_users = form.cleaned_data['shared_users']
            for shared_user in shared_users:
                SharedWith.objects.create(user_file=user_file, user=shared_user)

            # Добавляем сообщение об успехе
            messages.success(request, 'Файл успешно загружен.')

            # Перенаправляем пользователя на другую страницу, например на главную страницу
            return redirect('/users/files')  # 'home' замените на имя URL-адреса, на который вы хотите перенаправить пользователя

    # Если метод не POST (то есть GET), то отображаем пустую форму
    else:
        form = UserFileForm(user=request.user)
  # Получаем список файлов пользователя и файлы, которыми с ним поделились
    user_files_queryset = UserFile.objects.filter(
        Q(user=request.user) | Q(shared_with_entries__user=request.user)
    ).distinct()

    return render(request, 'users/user_files.html', {'form': form, 'user_files': user_files_queryset})


def view_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id, user=request.user)
    return render(request, 'users/view_file.html', {'user_file': user_file})


#def download(request, file_id):
    # Проверяем, есть ли у пользователя права на скачивание файла
    #user_file = get_object_or_404(UserFile, Q(id=file_id) & (Q(user=request.user) | Q(shared_with_entries__user=request.user)))

    #response = FileResponse(user_file.file)
    #response['Content-Disposition'] = f'attachment; filename="{user_file.name}"'
    #return response

from django.urls import reverse

def delete_file(request, file_id):
    if request.method == 'POST':
        user_file = get_object_or_404(UserFile, id=file_id, user=request.user)
        user_file.file.delete()  # Удаление файла из файловой системы
        user_file.delete()  # Удаление записи о файле из базы данных
        messages.success(request, 'Файл успешно удален.')
        
        # Обновляем список файлов пользователя после удаления
        user_files = UserFile.objects.filter(user=request.user)
        form = UserFileForm()

        return render(request, 'users/user_files.html', {'form': form, 'user_files': user_files})

    # Если мы здесь, значит был не POST-запрос, и мы просто перенаправляем на список файлов
    return redirect('user_files')

