from django.urls import path
from users.views import autorization, registration, user_files, delete_file, view_file #download
from . import views


app_name = 'users'

urlpatterns = [
    path('autorization/', autorization, name='autorization'),
    path('registration/', registration, name='registration'),
    path('files/', user_files, name='user_files'),  # Ensure this points to the user_files view function
    path('files/view/<int:file_id>/', view_file, name='view_file'),
    #path('files/download/<int:file_id>/', download, name='download'),  # Ensure this points to the download view function
    path('files/delete/<int:file_id>/', delete_file, name='delete_file'),  # URL для удаления файла
]
