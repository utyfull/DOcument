import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse
from .models import UserFile
from .forms import UserFileForm
from users.models import User, FileSignature
from users.forms import UserLoginForm, UserRegistrationForm, CommentForm
from django.http import FileResponse, QueryDict
from django.shortcuts import get_object_or_404
from .models import UserFile, SharedWith  # Убедитесь, что здесь импортирован SharedWith
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import PFXUploadForm
from OpenSSL import crypto
from .filters import fileFilter, foreign_fileFilter
from django.http import JsonResponse

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



@login_required
def user_files(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            user_file = form.save(commit=False)
            user_file.user = request.user
            user_file.save()

            shared_users = form.cleaned_data['shared_users']
            for shared_user in shared_users:
                SharedWith.objects.get_or_create(user_file=user_file, user=shared_user)

            # Добавляем сообщение об успехе
            messages.success(request, 'Файл успешно загружен.')

            # Перенаправляем пользователя на другую страницу, например на главную страницу
            return redirect('/users/files')  # 'home' замените на имя URL-адреса, на который вы хотите перенаправить пользователя

    else:
        form = UserFileForm(user=request.user)

    # Получаем список файлов пользователя и файлы, которыми с ним поделились
    user_files_queryset = UserFile.objects.filter(
        Q(user=request.user) | Q(shared_with_entries__user=request.user)
    ).distinct()

    first_filter = fileFilter(request.GET, prefix='first', queryset=user_files_queryset)
    second_filter = foreign_fileFilter(request.GET, prefix='second', queryset=user_files_queryset)

    return render(request, 'users/user_files.html', {'form': form, 'first_filter': first_filter, 'second_filter': second_filter})

@login_required
def remove_shared_user(request, file_id, user_id):
    user_file = get_object_or_404(UserFile, id=file_id, user=request.user)
    shared_user = get_object_or_404(User, id=user_id)
    SharedWith.objects.filter(user_file=user_file, user=shared_user).delete()
    messages.success(request, f'Пользователь {shared_user.username} был удален из списка доступа к файлу.')
    return redirect('/users/files')



@login_required
#Камила,ничего не меняй(пока)
def view_own_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id)
    pfx_form = PFXUploadForm()
    comment_form = CommentForm()

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

    comments = user_file.comments.all()

    return render(request, 'users/view_file.html', {
        'user_file': user_file,
        'pfx_form': pfx_form,
        'comment_form': comment_form,
        'comments': comments,
    })


@login_required
def view_foreign_file(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id)
    pfx_form = PFXUploadForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'pfx_file' in request.FILES:
            if FileSignature.objects.filter(user=request.user, user_file=user_file).exists():
                messages.error(request, 'Вы уже подписали этот файл.')
                return redirect('users:view_foreign_file', file_id=user_file.id)

            pfx_form = PFXUploadForm(request.POST, request.FILES)
            if pfx_form.is_valid():
                try:
                    pfx_file = request.FILES['pfx_file']
                    password = pfx_form.cleaned_data['password']
                    pfx_data = pfx_file.read()

                    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
                        pfx_data, password.encode()
                    )

                    file_content = user_file.content or ""
                    file_content_bytes = file_content.encode()

                    sign = private_key.sign(
                        file_content_bytes,
                        padding.PKCS1v15(),
                        hashes.SHA256()
                    )

                    # Сохраняем информацию о подписавшем пользователе
                    FileSignature.objects.create(user=request.user, user_file=user_file)

                    messages.success(request, 'Файл успешно подписан.')
                    return redirect('users:view_foreign_file', file_id=user_file.id)
                except Exception as e:
                    messages.error(request, f'Не удалось извлечь ключ из PFX файла. Проверьте правильность пароля. Ошибка: {e}')
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.user_file = user_file
                comment.save()
                messages.success(request, 'Комментарий добавлен.')
                return redirect('users:view_foreign_file', file_id=user_file.id)

    comments = user_file.comments.all()
    signatures = FileSignature.objects.filter(user_file=user_file)
    users = User.objects.all()

    return render(request, 'users/shared_file_detail.html', {
        'user_file': user_file,
        'pfx_form': pfx_form,
        'comment_form': comment_form,
        'comments': comments,
        'signatures': signatures,
        'users': users,
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
        user_file.delete()  # Удаление записи о файле из базы данных
        messages.success(request, 'Файл успешно удален.')

        # Переадресация на страницу со списком файлов
        return redirect('users:user_files')  # 'user_files' - это имя маршрута, который ведет к списку файлов

    # Если метод запроса не POST, перенаправляем на страницу со списком файлов
    return redirect('users:user_files')

@login_required
def editor(request):
    return render(request, 'editor.html')


@login_required
def save_document(request):
    if request.method == 'POST' and request.is_ajax():
        html_content = request.POST.get('html_content')

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': {'Invalid request'}})

