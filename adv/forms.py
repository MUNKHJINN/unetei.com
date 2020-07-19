from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ad, Pic
from django import forms


class FileFieldForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Pic
        fields = ['url']


class AdForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': ' Гарчиг...', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Тайлбар...', 'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Холбоо барих утас...', 'class': 'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Үнэ...', 'class': 'form-control'}))
    url = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'multiple': True, 'class': 'form-control'}))

    class Meta:
        model = Ad
        fields = ['cat', 'sub', 'title', 'description', 'phone_number', 'price', 'url']


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput
    (attrs={'placeholder': 'Хэрэглэгчийн нэр...', 'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput
    (attrs={'placeholder': 'И-мэйл хаяг', 'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.TextInput
    (attrs={'placeholder': 'Нууц үг...', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.TextInput
    (attrs={'placeholder': 'Нууц үг... (Давтах)', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

