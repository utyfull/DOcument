import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from .models import UserFile
from .forms import UserFileForm
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, CommentForm
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import UserFile, SharedWith  # Убедитесь, что здесь импортирован SharedWith
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import PFXUploadForm
from OpenSSL import crypto
from .tasks import send_custom_email


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
            send_custom_email("Registration", f"Now you are with us! <DOcument>", [form.cleaned_data['username']])
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
    # Получаем объект файла для просмотра
    user_file = get_object_or_404(UserFile, id=file_id, shared_with_entries__user=request.user)
    pfx_form = PFXUploadForm()

    if request.method == 'POST':
        pfx_form = PFXUploadForm(request.POST, request.FILES)
        if pfx_form.is_valid():
            try:
                pfx_file = request.FILES['pfx_file']
                password = pfx_form.cleaned_data['password']
                pfx_data = pfx_file.read()

                # Загрузка PFX файла и извлечение ключа и сертификата
                private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                    pfx_data, password.encode()
                )

                # Подписываем файл
                sign = private_key.sign(
                    user_file.content.encode(),
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )

                # Заменяем содержимое оригинального файла на подписанное
                signed_content = user_file.content + '\n\nSignature:\n' + base64.b64encode(sign).decode()
                user_file.content = signed_content
                user_file.save()

                messages.success(request, 'Файл успешно подписан.')
                return redirect('users:view_foreign_file', file_id=user_file.id)  # Перенаправляем на страницу просмотра файла
            except Exception as e:
                messages.error(request,
                               f'Не удалось извлечь ключ из PFX файла. Проверьте правильность пароля. Ошибка: {e}')

    return render(request, 'users/shared_file_detail.html', {
        'user_file': user_file,
        'pfx_form': pfx_form
    })


@login_required
def view_foreign_file(request, file_id):
    # Получаем объект файла для просмотра
    user_file = get_object_or_404(UserFile, id=file_id, shared_with_entries__user=request.user)
    pfx_form = PFXUploadForm()

    if request.method == 'POST':
        pfx_form = PFXUploadForm(request.POST, request.FILES)
        if pfx_form.is_valid():
            try:
                pfx_file = request.FILES['pfx_file']
                password = pfx_form.cleaned_data['password']
                pfx_data = pfx_file.read()

                # Загрузка PFX файла и извлечение ключа и сертификата
                private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                    pfx_data, password.encode()
                )

                # Чтение содержимого файла, если оно пустое, устанавливаем значение по умолчанию
                file_content = user_file.content or ""
                file_content_bytes = file_content.encode()  # Преобразуем текстовое содержимое в байты

                # Подписываем файл
                sign = private_key.sign(
                    file_content_bytes,
                    padding.PKCS1v15(),
                    hashes.SHA256()
                )

                # Создание подписанного содержимого
                signed_content = file_content_bytes + b'\n\nSignature:\n' + base64.b64encode(sign)

                # Сохранение подписанного содержимого
                user_file.content = signed_content.decode()  # Преобразуем байты обратно в текст
                user_file.save()

                messages.success(request, 'Файл успешно подписан.')

                if request.user.is_authenticated:
                    send_custom_email("Document sign", f"you sign document {user_file.name}", [request.user.username])
                    send_custom_email("Document sign", f"User {request.user.username} have signed file {user_file.name}", [])
                return redirect('users:view_foreign_file', file_id=user_file.id)  # Перенаправляем на страницу просмотра файла
            except Exception as e:
                messages.error(request, f'Не удалось извлечь ключ из PFX файла. Проверьте правильность пароля. Ошибка: {e}')

    return render(request, 'users/shared_file_detail.html', {
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

