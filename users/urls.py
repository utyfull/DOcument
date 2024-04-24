from django.urls import path
from users.views import autorization, registration

app_name = 'users'

urlpatterns = [
    path('autorization/', autorization, name='autorization'),
    path('registration/', registration, name='registration'),
]