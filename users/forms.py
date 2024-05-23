from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserFile
from users.models import User
from django.contrib.auth import get_user_model
from django_select2.forms import Select2MultipleWidget


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ('username', 'password')



class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'confirm password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')






UserModel = get_user_model()

class UserFileForm(forms.ModelForm):
    shared_users = forms.ModelMultipleChoiceField(
        queryset=UserModel.objects.none(),  # Изначально устанавливаем пустой queryset
        required=False,
        widget=Select2MultipleWidget
    )

    class Meta:
        model = UserFile
        fields = ['file', 'shared_users']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Извлекаем пользователя из kwargs
        super(UserFileForm, self).__init__(*args, **kwargs)  # Не забываем вызвать метод super
        
        if user is not None:
            # Теперь устанавливаем queryset для поля shared_users, исключив текущего пользователя
            self.fields['shared_users'].queryset = UserModel.objects.exclude(id=user.id)


class PFXUploadForm(forms.Form):
    pfx_file = forms.FileField(label='Select your .pfx certificate')