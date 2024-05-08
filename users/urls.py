from django.urls import path
from users.views import autorization, registration
from . import views


app_name = 'users'

urlpatterns = [
    path('autorization/', autorization, name='autorization'),
    path('user_files/', views.user_files, name='user_files'),
    path('registration/', registration, name='registration'),
    path('upload/', views.upload_file, name='upload_file'),
]
