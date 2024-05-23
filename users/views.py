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
from django.contrib.auth.decorators import login_required
from .forms import PFXUploadForm
from OpenSSL import crypto


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


@login_required
def view_own_file(request, file_id):
    # Получаем объект файла для просмотра
    user_file = get_object_or_404(UserFile, id=file_id)
    pfx_form = PFXUploadForm()

    if request.method == 'POST':
        pfx_form = PFXUploadForm(request.POST, request.FILES)
        if pfx_form.is_valid():
            try:
                pfx_file = request.FILES['pfx_file']
                pfx = crypto.load_pkcs12(pfx_file.read())
                signer = pfx.get_privatekey()

                # Подписываем файл
                sign = crypto.sign(signer, user_file.content, 'sha256')

                # Сохраняем подписанный файл (нужно реализовать функцию save_signed_file)
                signed_file_path = save_signed_file(user_file.content, sign)

                messages.success(request, 'Файл успешно подписан.')
                return redirect('signed_file_download', file_path=signed_file_path)

            except Exception as e:
                messages.error(request, 'Не удалось извлечь ключ из PFX файла.')

    return render(request, 'users/view_file.html', {
        'user_file': user_file,
        'pfx_form': pfx_form
    })


def view_foreign_file(request, file_id):
    # Получаем объект файла для просмотра
    user_file = get_object_or_404(UserFile, id=file_id)
    pfx_form = PFXUploadForm()

    if request.method == 'POST':
        pfx_form = PFXUploadForm(request.POST, request.FILES)
        if pfx_form.is_valid():
            try:
                pfx_file = request.FILES['pfx_file']
                pfx = crypto.load_pkcs12(pfx_file.read())
                signer = pfx.get_privatekey()

                # Подписываем файл
                sign = crypto.sign(signer, user_file.content, 'sha256')

                # Сохраняем подписанный файл (нужно реализовать функцию save_signed_file)
                signed_file_path = save_signed_file(user_file.content, sign)

                messages.success(request, 'Файл успешно подписан.')
                return redirect('signed_file_download', file_path=signed_file_path)

            except Exception as e:
                messages.error(request, 'Не удалось извлечь ключ из PFX файла.')

    return render(request, 'users/view_file.html', {
        'user_file': user_file,
        'pfx_form': pfx_form
    })


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
        user_file.delete()  # Удаление записи о файла из базы данных
        messages.success(request, 'Файл успешно удален.')

        # Переадресация на страницу со списком файлов
        return redirect('users:user_files')  # 'user_files' - это имя маршрута, который ведет к списку файлов

    # Если метод запроса не POST, перенаправляем на страницу со списком файлов
    return redirect('users:user_files')


def handle_pfx_file(f, file_to_sign_path):
    # Здесь была бы логика подписания файла.
    pass


def sign_file(request, file_id):
    file_to_sign = get_file_by_id(file_id)

    if request.method == 'POST':
        form = PFXUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                pfx_file = request.FILES['pfx_file']
                pfx = crypto.load_pkcs12(pfx_file.read(), passphrase=b'')
                signer = pfx.get_privatekey()
                certificate = pfx.get_certificate()

                sign = crypto.sign(signer, file_to_sign, 'sha256')

                save_signed_file(file_to_sign, sign, certificate)

                # Перенаправляем пользователя на страницу с подписанным файлом
                return redirect('signed_file_page', file_id=file_id)
            except Exception as e:
                error_message = str(e)
    else:
        form = PFXUploadForm()

    return render(request, 'sign_file.html', {'form': form, 'error_message': error_message})
