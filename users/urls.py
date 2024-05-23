from django.urls import path
from django.urls import include
from users.views import autorization, registration, user_files, delete_file, view_file #download
from . import views
from .views import sign_file



app_name = 'users'

urlpatterns = [
    path('autorization/', autorization, name='autorization'),
    path('registration/', registration, name='registration'),
    path('files/', user_files, name='user_files'),  # Ensure this points to the user_files view function
    path('files/view/<int:file_id>/', view_file, name='view_file'),  # Добавлен параметр <int:file_id>/
    path('files/delete/<int:file_id>/', delete_file, name='delete_file'),
    path('files/<int:document_id>/sign/', sign_file, name='sign_file'),


    # URL для удаления файла
]
